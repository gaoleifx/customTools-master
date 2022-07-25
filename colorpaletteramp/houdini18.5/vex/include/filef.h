#ifndef __file_h__
#define __file_h__

/*
 * PROPRIETARY INFORMATION.  This software is proprietary to
 * Side Effects Software Inc., and is not to be reproduced,
 * transmitted, or disclosed in any way without written permission.
 *
 * Produced by:
 *	Side Effects Software Inc
 *	477 Richmond Street West
 *	Toronto, Ontario
 *	Canada   M5V 3E7
 *	416-504-9876
 *
 * NAME:	file.h (VEX)
 *
 * COMMENTS:	This include file contains constants used by file functions
 */

#define STAT_FILETYPE_INVALID	-1
#define STAT_FILETYPE_REGULAR	0
#define STAT_FILETYPE_DIR	1

#define STAT_FIELD_MODE		0
#define STAT_FIELD_FILETYPE	1
#define STAT_FIELD_SIZE		2
#define STAT_FIELD_SIZEMB	3
#define STAT_FIELD_MTIME	4

#define STAT_MODE_EXECUTE	0x01
#define STAT_MODE_WRITE		0x02
#define STAT_MODE_READ		0x04

struct stat
{
    /// Perform a stat of the given file
    void	init(string name)
    {
	int	data[];
	st_name = name;
	if (file_stat(name, data))
	{
	    st_mode = data[STAT_FIELD_MODE];
	    st_filetype = data[STAT_FIELD_FILETYPE];
	    st_size = data[STAT_FIELD_SIZE];
	    st_sizemb = data[STAT_FIELD_SIZEMB];
	    st_mtime = data[STAT_FIELD_MTIME];
	}
	else
	{
	    st_mode = 0;
	    st_filetype = STAT_FILETYPE_INVALID;
	    st_size = 0;
	    st_sizemb = 0;
	    st_mtime = 0;
	}
    }
    /// Perform stat using cached versions of the stat.  The cache is
    /// persistent over the entire run of the application.
    void	initCached(string name)
    {
	int	data[];
	st_name = name;
	if (file_stat(name, data, "usecache", 1))
	{
	    st_mode = data[STAT_FIELD_MODE];
	    st_filetype = data[STAT_FIELD_FILETYPE];
	    st_size = data[STAT_FIELD_SIZE];
	    st_sizemb = data[STAT_FIELD_SIZEMB];
	    st_mtime = data[STAT_FIELD_MTIME];
	}
	else
	{
	    st_mode = 0;
	    st_filetype = STAT_FILETYPE_INVALID;
	    st_size = 0;
	    st_sizemb = 0;
	    st_mtime = 0;
	}
    }
    int		isValid()
		    { return st_filetype != STAT_FILETYPE_INVALID; }
    int		isFile()
		    { return st_filetype == STAT_FILETYPE_REGULAR; }
    int		isDir()
		    { return st_filetype == STAT_FILETYPE_DIR; }
    int		isRead()
		    { return st_mode & STAT_MODE_READ; }
    int		isWrite()
		    { return st_mode & STAT_MODE_WRITE; }
    int		isExecute()
		    { return st_mode & STAT_MODE_WRITE; }

    void	dump()
    {
	printf("%s {\n"
		"  mode: %x\n"
		"  type: %d\n"
		"  size: %d (bytes)\n"
		"  size: %d (MB)\n"
		"  mtime: %d\n"
		"}\n",
		st_name, st_mode, st_filetype, st_size, st_sizemb, st_mtime);
    }


    string	st_name;	// Filename
    int		st_mode;	// Permissions
    int		st_filetype;	// The file type
    int		st_size;	// Size in bytes (clamped at max integer)
    int		st_sizemb;	// Size in MB (ceil(size/(1024*1024)))
    int		st_mtime;	// Time of last modification
};

stat
file_stat(string name)
{
    stat	sbuf;
    sbuf->init(name);
    return sbuf;
}

stat
cached_file_stat(string name)
{
    stat	sbuf;
    sbuf->initCached(name);
    return sbuf;
}

#endif
