def deriveFeedNameAndSourceData(file_name):

    """Derives the feed name and source data from a given filename."""

    feed_name = file_name[:file_name.rindex('_')]
    source_data_mth = file_name[file_name.rindex('_')+1:file_name.rindex('_')+1+6]
    source_data_dt = file_name[file_name.rindex('_')+1:file_name.rindex('_')+1+8]
    source_data_tms = file_name[file_name.rindex('_')+1:file_name.rindex('_')+1+14]

    return  feed_name, source_data_mth, source_data_dt, source_data_tms

