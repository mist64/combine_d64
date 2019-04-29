# `combine_d64` D64 File Reconstruction Tool

This tools helps reconstructing a correct Commodore 1541 `.D64` image from multiple copies by comparing different copies block by block.

There are two use cases:

## Preserving Commercial Software

If you want to preserve original commercial 1541 disks, you should make sure the image you are creating is correct. If all you have a single copy of the original disk, even without any read errors, some blocks might still have been changed by the user.

If you have multiple copies of the original disk, and two (or better: three) of them are identical, you can be fairly confident you have a correct dump.

But if all your copies have changed or broken blocks, you might still be lucky as long as these are not the same across disks. This is where this tool helps.

## Rescuing Broken Disks

If you have a (personal data) disk that has lots of read errors, the first step (after thoroughly cleaning your read head with alcohol!) would be to maximize the number of retries when reading it. You could also read it in different drives and see which one gives you the best result.

But oftentimes, different read attempts give you a different distribution of broken blocks. This tool helps you combine the correct data across multiple images with errors.

## Usage

	python combine_d64.py <file1.d64> <file2.d64> [...]

Depending on the input files, you will get one of these results:

### 1. Identical Images

	The following images are identical:
	05b.d64 14b.d64

Two or more images are identical, and all other images are different. You can assume you have two correct reads, and you can take any of the correct files as your result.

### 2. Identical Image Sets

	The following sets of images are identical:
	0 : 42b.d64 45b.d64
	1 : 44b.d64 46b.d64

Two or more images are identical, but there are other identical sets as well. One of the sets _may_ be correct. This usually happens in the "Preserving Commercial Software" case if you different users made the same changes to a disk. You will need to look at the differences between the sets and decide which one (if any) is the original state.

### 3. Image of Duplicate Blocks

	Every block of the following images is also contained in at least one other file:
	48a.d64

There is one image whose every block exists as a duplicate in another image. This is a good indication that this image is a correct read, and you can take it as the result.

### 4. Combined Image

	The result was combined from the following images:
	41ad64 (667 blocks)
	42ad64 (16 blocks)

Of every block, there are at least two identical copies across the disks. The tool creats "result.d64" with the combined data and prints which images were used for how many blocks.

### 5. Not Enough Duplicates

	For the following blocks, no duplicates exist:
	400 (Trk 20 Sec 5)

If there are not at least two identical copies of every block, the tool prints out the block numbers (and track/sector) of the blocks that need more copies.

### Warnings

For cases 3 and 4, the tool also prints a list of blocks for which there were only 2 identical copies. You might want to be careful with these blocks and double-check they are not caused by identical changes by different users ("Preserving Commercial Software" case).

	The following blocks only had a limited number of copies:
	2 copies of block 125 (Trk 6 Sec 20) in 48a.d64 51a.d64
	2 copies of block 357 (Trk 18 Sec 0) in 48a.d64 50a.d64
	2 copies of block 358 (Trk 18 Sec 1) in 48a.d64 50a.d64

## Limitations

Also note that commercial disks might be using copy protection tricks that cannot be represented in `.D64` images. You will need `.G64` images for this. You can use this tool on the `.D64` versions, so it can tell you which corresponding `.G64` file is most likely the correct one. If the tool creates a combined "result.d64" file, you can use [g64conv](https://github.com/markusC64/g64conv) to manually create a correct `.G64` file from it.

There has been only limited testing, especially on images with errors. Use at your own risk, and verify the results manually, especially in case 4!

## Credits

Written by Michael Steil <mist64@mac.com>, [www.pagetable.com](https://www.pagetable.com/), Public Domain.

Contributions welcome!