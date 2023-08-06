#!/usr/bin/env python3

import os, sys
from datetime import datetime, timezone
from optparse import OptionParser
from subprocess import Popen, PIPE, STDOUT
from markdown import Markdown
from glob import glob
from re import compile

HOOKPOINT_INIT = 0
HOOKPOINT_PARSE = 1

def extFileName(*args):
	if args[0] == HOOKPOINT_PARSE:
		filename, stack, files, options = args[1:5]
		bname = os.path.basename(filename)
		fname, fext = os.path.splitext(bname)

		files[filename]['input-path'] = filename
		files[filename]['input-name'] = fname
		files[filename]['input-ext'] = fext
		files[filename]['input-basename'] = bname

		if options.output:
			bname = os.path.basename(options.output)
			fname, fext = os.path.splitext(bname)

			files[filename]['output-path'] = options.output
			files[filename]['output-name'] = fname
			files[filename]['output-ext'] = fext
			files[filename]['output-basename'] = bname

def extDate(*args):
	if args[0] == HOOKPOINT_PARSE:
		filename, stack, files, options = args[1:5]
		stat = os.stat(filename)
		files[filename]['input-date'] = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).strftime(options.date_fmt)

def extGitDate(*args):
	if args[0] == HOOKPOINT_PARSE:
		filename, stack, files, options = args[1:5]
		p = Popen(['git', '--git-dir="%s"' % options.git_dir, 'log', '-1', '"--date=format:%s"' % options.date_fmt, '--format=%cd', filename], stdout=PIPE, stderr=PIPE)
		gitStdOut, gitStdErr = p.communicate()
		files[filename]['input-git-date'] = ('<font color="red">%s</font>' % gitStdErr.decode()) if gitStdErr else gitStdOut.decode()

def extCustom(*args):
	if args[0] == HOOKPOINT_INIT:
		parser = args[1]
		parser.add_option('-a', '--add', dest='params', action="append", help='Add parameter in format name:value')

	if args[0] == HOOKPOINT_PARSE:
		filename, stack, files, options = args[1:5]
		if options.params:
			for p in options.params:
				name, value = p.split(':')
				files[filename][name] = value

# example: %(input-file-date:1.md)s
extMetaPattern = compile('%\((([^:\)]+):([^:\)]+))\)')

def extMeta(*args):
	if args[0] == HOOKPOINT_PARSE:
		filename, stack, files, options = args[1:5]
		sourceDir = os.path.dirname(options.source)
		for it in extMetaPattern.finditer(files[filename]['source']):
			if options.trace:
				print('[meta] triggered on %s at %s' % (it.group(0), it.span(0)), file=sys.stderr)

			name = it.group(2)
			path = it.group(3)
			dependency = '%s/%s' % (sourceDir, path)
			stack.append(dependency)
			if dependency not in files[filename]['dependencies']:
				files[filename]['dependencies'][dependency] = []

			files[filename]['dependencies'][dependency].append((it.group(1), name, lambda a, b: b))

# example: %(glob:row:*.md)s
extGlobPattern = compile('%\((glob:([^:\)]+):([^:\)]+))\)')

def extGlob(*args):
	if args[0] == HOOKPOINT_INIT:
		parser = args[1]
		parser.add_option('-g', '--git-dir', dest='git_dir', default='%s/.git' % os.path.dirname(sys.argv[0]), help='Set GIT directory location, e.g. /home/user/repo/.git')

	if args[0] == HOOKPOINT_PARSE:
		filename, stack, files, options = args[1:5]
		sourceDir = os.path.dirname(options.source)
		for it in extGlobPattern.finditer(files[filename]['source']):
			if options.trace:
				print('[glob] triggered on %s at %s' % (it.group(0), it.span(0)), file=sys.stderr)

			name = it.group(2)
			mask = it.group(3)

			if options.trace:
				print('[glob] glob path %s/%s' % (sourceDir, mask), file=sys.stderr)

			for g in glob('%s/%s' % (sourceDir, mask)):
				if options.trace:
					print('[glob] add dependency from %s: %s, %s' % (g, it.group(1), name), file=sys.stderr)

				stack.append(g)
				if g not in files[filename]['dependencies']:
					files[filename]['dependencies'][g] = []

				files[filename]['dependencies'][g].append((it.group(1), name, lambda a, b: a + b))

extensions = {
	'filename': extFileName,
	'date': extDate,
	'gitdate': extGitDate,
	'custom': extCustom,
	'meta': extMeta,
	'glob': extGlob,
}

def main(options):
	if options.source is None or options.html is None or options.trace is None or options.markdown_ext is None or options.date_fmt is None or options.ext is None:
		print('error: invalid parameter', file=sys.stderr)
		return False

	hooks = []
	files = {}
	stack = [options.source]

	if options.ext:
		for e in list(set(options.ext.split(','))):
			if e not in extensions:
				print('error: invalid extension "%s"' % e, file=sys.stderr)
				return False

			hooks.append(extensions[e])

	with open(options.html) as f:
		html = f.read()

	while len(stack):
		filename = stack[-1]
		stack = stack[:-1]

		if options.trace:
			print('parse %s...' % filename, file=sys.stderr)

		with open(filename) as f:
			files[filename] = {
				'dependencies': {},
				'source': f.read(),
			}

		# hook point
		for hook in hooks:
			hook(HOOKPOINT_PARSE, filename, stack, files, options)

	while len(files):

		indep = [filename for filename in files if len(files[filename]['dependencies']) == 0]
		if len(indep) == 0:
			print('error: dependency loop', file=sys.stderr)
			return False

		filename = indep[0]

		if options.trace:
			print('generate %s...' % filename, file=sys.stderr)

		if 'document' not in files[filename]:
			md = Markdown(extensions=options.markdown_ext.split(','))

			files[filename]['body'] = md.convert(files[filename]['source'])

			if md.Meta:
				toFormat = []
				for metaName in md.Meta:
					if len(md.Meta[metaName]) == 1:
						files[filename][metaName] = md.Meta[metaName][0]
						toFormat.append(metaName)
					else:
						for idx, meta in enumerate(md.Meta[metaName]):
							idxMetaName = '%s[%u]' % (metaName, idx)
							files[filename][idxMetaName] = meta
							toFormat.append(idxMetaName)

				if options.trace:
					print('format metadata: %s...' % toFormat, file=sys.stderr)

				for metaName in toFormat:
					files[filename][metaName] = files[filename][metaName] % files[filename]

			files[filename]['body'] = files[filename]['body'] % files[filename]
			files[filename]['document'] = html % files[filename]
	
		for i in files:
			if filename in files[i]['dependencies']:
				if options.trace:
					print('update dependencies for %s (%s)...' % (i, len(files[i]['dependencies'][filename])), file=sys.stderr)

				for dst, src, action in files[i]['dependencies'][filename]:
					if options.trace:
						print('set %%(%s)=%%(%s)' % (dst, src), file=sys.stderr)

					files[i][dst] = action(files[i][dst] if (dst in files[i]) else '', files[filename][src])
				del files[i]['dependencies'][filename]

		if filename == options.source:
			if options.output:
				with open(options.output, 'w') as f:
					f.write(files[filename]['document'])
			else:
				print(files[filename]['document'])
			break

		del files[filename]

	return True

def main_m():
	parser = OptionParser(usage="python -m mdhtmlgen [options]")
	parser.add_option('-S', '--source', dest='source', help='Markdown source filename (*.md)')
	parser.add_option('-H', '--html', dest='html', help='HTML template filename (*.t)')
	parser.add_option('-t', '--trace', dest='trace', action='store_true', default=False, help='Print diagnostic traces')
	parser.add_option('-o', '--output', dest='output', help='Set output file')
	parser.add_option('-m', '--markdown-ext', dest='markdown_ext', default='', help='Set markdown extension list, coma separated, e.g. meta,toc,footnotes')
	parser.add_option('-d', '--date-fmt', dest='date_fmt', default='%d-%m-%Y %H:%M:%S', help='Set date format, e.g. %d-%m-%Y %H:%M:%S')
	parser.add_option('-e', '--ext', dest='ext', default='', help='Set extension list, e.g. meta,glob,filename,date')

	# hook point
	for hook in extensions:
		extensions[hook](HOOKPOINT_INIT, parser)

	(options, args) = parser.parse_args()

	if options.source is None or options.html is None:
		parser.print_help()
		exit(1)

	if not main(options):
		exit(1)

if __name__ == '__main__':
	main_m()
