mklinks: tool for finding and hardlinking identical files

*Latest release 20210306*:
Use cs.cmdutils.BaseCommand for main programme, add better progress reporting.

Mklinks walks supplied paths looking for files with the same content,
based on a cryptographic checksum of their content. It hardlinks
all such files found, keeping the newest version.

Unlike some rather naive tools out there, mklinks only compares
files with other files of the same size, and is hardlink aware - a
partially hardlinked tree is processed efficiently and correctly.

## Class `FileInfo`

Information about a particular inode.

### Method `FileInfo.assimilate(self, other, no_action=False)`

Link our primary path to all the paths from `other`. Return success.

### Method `FileInfo.same_dev(self, other)`

Test whether two FileInfos are on the same filesystem.

### Method `FileInfo.same_file(self, other)`

Test whether two FileInfos refer to the same file.

### Method `FileInfo.stat_key(S)`

Compute the key `(dev,ino)` from the stat object `S`.

## Class `Linker`

The class which links files with identical content.

### Method `Linker.addpath(self, path)`

Add a new path to the data structures.

### Method `Linker.merge(self, *a, **kw)`

Merge files with equivalent content.

### Method `Linker.scan(self, *a, **kw)`

Scan the file tree.

## Function `main(argv=None)`

Main command line programme.

## Class `MKLinksCmd(cs.cmdutils.BaseCommand)`

Main programme command line class.

### Method `MKLinksCmd.apply_defaults(self)`

Set up the default values in `options`.

### Method `MKLinksCmd.apply_opts(self, opts)`

Apply command line options.

### Method `MKLinksCmd.main(self, argv)`

Usage: mklinks [-n] paths...
Hard link files with identical contents.
-n    No action. Report proposed actions.

# Release Log



*Release 20210306*:
Use cs.cmdutils.BaseCommand for main programme, add better progress reporting.

*Release 20171228*:
Initial PyPI release of cs.app.mklinks.
