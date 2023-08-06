"""Defines all functions within the s3 (simple storage service) module."""

# Standard library imports
import os
from io import BytesIO, StringIO
from tempfile import TemporaryFile, NamedTemporaryFile
from pickle import dumps
from logging import getLogger
from time import time

# Related third party imports
from boto3 import client, resource
from numpy import load, save, savez
from h5py import File as s3File
from s3fs import S3FileSystem

# from sklearn.externals import joblib
from pandas import (
    DataFrame,
    read_csv,
    read_excel,
    read_pickle,
    read_hdf,
    ExcelWriter,
    HDFStore,
)


def export_file(obj, bucket: str, s3key: str, **kwargs):
    """Export python object to specified location in AWS S3.

    Keyword Arguments:
        - obj       - Python object to be exported
        - bucket    - S3 export bucket,no trailing "/"
        - s3key     - S3 export key, no leading "/". String should end with the
                      desired file format. "public/.../example.csv".
                      Currently supported fileformats are
                        - .csv
                            - pandas.DataFrame()
                        - .xlsx
                            - pandas.DataFrame()
                        - .pkl
                            - pandas.DataFrame()
                            - sklearn (temporarly removed)
                        - .h5
                            - pandas.DataFrame()
                        - .npy
                            - numpy (arrays)
                        - .npz
        - **kwargs
    """
    # Initiate Logger
    logger = getLogger(__name__)
    start = time()

    # Connect to S3
    s3resource = resource("s3")

    # Extra file name, file format and export object type
    _, file_fmt = os.path.splitext(s3key)
    obj_class = obj.__class__.__module__.split(".")[0]

    logger.info(
        """Load settings:\n\tobj_class=%s\n\tbucket=%s\n\ts3key=%s""",
        obj_class,
        bucket,
        s3key,
    )
    logger.info("Exporting %s-data to S3:", file_fmt)

    # Comma separated files
    if (file_fmt == ".csv") & (obj_class == "pandas"):
        buffer = StringIO()
        obj.to_csv(buffer, index=False, **kwargs)
        s3resource.Object(bucket, s3key).put(Body=buffer.getvalue())

    # Excel files
    elif (file_fmt == ".xlsx") & (obj_class == "pandas"):
        with BytesIO() as output:
            with ExcelWriter(output, engine="xlsxwriter") as writer:
                obj.to_excel(writer, **kwargs)
            data = output.getvalue()
            s3resource.Object(bucket, s3key).put(Body=data)

    # Pickle files
    # elif (file_fmt == ".pkl") & (obj_class == "sklearn"):
    #     with TemporaryFile() as temp_file:
    #         joblib.dump(obj, temp_file)
    #         temp_file.seek(0)
    #         s3resource.Object(bucket, s3key).put(Body=temp_file.read())

    elif (file_fmt == ".pkl") & (obj_class == "pandas"):
        serialized_data = dumps(obj)
        s3resource.Object(bucket, s3key).put(Body=serialized_data)

    # HDF5 files
    elif (file_fmt == ".h5") & (obj_class == "pandas"):
        with NamedTemporaryFile(suffix=".h5") as temp_file:
            hdf = HDFStore(temp_file.name)
            hdf.put(value=obj, format="table", data_columns=True, **kwargs)
            hdf.close()
            temp_file.seek(0)
            s3resource.Object(bucket, s3key).put(Body=temp_file.read())

    # npy files
    elif (file_fmt == ".npy") & (obj_class == "numpy"):
        with TemporaryFile() as temp_file:
            save(temp_file, obj)
            temp_file.seek(0)
            s3resource.Object(bucket, s3key).put(Body=temp_file.read())

    # npz files- This exports each pandas column to a compressed numpy array
    # as a "key-value pair". See numpy documentation for more information
    elif (file_fmt == ".npz") & (obj_class == "pandas"):
        with TemporaryFile() as temp_file:
            savez(temp_file, **obj.to_dict())
            temp_file.seek(0)
            s3resource.Object(bucket, s3key).put(Body=temp_file.read())

    else:
        raise_str = f"""Failed! {file_fmt} export of {obj_class} objects not
            implemented."""
        logger.info("\tFailed! %s", raise_str)
        raise Exception()

    logger.info("\tOK! Exported data in %f [s]", time() - start)


def import_file(bucket: str, s3key: str, obj_class: str = "pandas", **kwargs):
    """Import DataFrame from specified bucket/s3key.

    Function imports data from specified bucket/s3 key combination based on
    the ending file format of the passed s3key.

    Arguments:
        - bucket    -   S3 export bucket, no trailing "/"
        - s3key     -   S3 export key, no leading "/" String should end with
                        the desired file format like "public/.../example.csv"
                        Currently supported fileformats is:
                            - .csv
                                - pandas.DataFrame()
                            - .xlsx
                                - pandas.DataFrame()
                            - .pkl
                                - pandas.DataFrame()
                                - sklearn.joblib (temporarly removed)
                            - .h5
                                - pandas.DataFrame()
                            - .npy
                                - numpy (array)
                            - .npz
                                - numpy-zip (arrays)
        - obj_class -   String explaining what object type file should be
                        loaded as (default = "pandas")
    Keyword Arguments:
        - **kwargs  -   Keyword arguments import function. Import function
                        varies for each file format:
                            - .csv  = pd.read_csv()
                            - .xlsx = pd.read_excel()
                            - .pkl  = pd.read_pickle()
                            - .h5   = pd.read_hdf()
    Returns:
        - obj       -   Imported object
    """
    # Initiate Logger
    logger = getLogger(__name__)
    start = time()

    # Extra file name, file format and export object type
    _, file_fmt = os.path.splitext(s3key)
    file_name = os.path.basename(s3key)
    s3client = client("s3")

    logger.info(f"Loading {file_name} ({file_fmt}) from S3:")
    logger.debug(
        """\tSettings used: obj_class = %s, bucket = %s, s3key = %s""",
        obj_class,
        bucket,
        s3key,
    )

    obj = DataFrame()

    # Get object if any of the specified formats
    if file_fmt in [".csv", ".xlsx", ".pkl"]:

        s3_obj = s3client.get_object(Bucket=bucket, Key=s3key)

        # csv files
        if (file_fmt == ".csv") & (obj_class == "pandas"):
            obj = read_csv(BytesIO(s3_obj["Body"].read()), **kwargs)

        # Excel files
        elif (file_fmt == ".xlsx") & (obj_class == "pandas"):
            obj = read_excel(BytesIO(s3_obj["Body"].read()), **kwargs)

        # Pickle files
        elif (file_fmt == ".pkl") & (obj_class == "pandas"):
            obj = read_pickle(BytesIO(s3_obj["Body"].read()), **kwargs)

    # HDF5 files
    elif (file_fmt == ".h5") & (obj_class == "pandas"):
        with NamedTemporaryFile() as temp_file:
            s3client.download_fileobj(
                Bucket=bucket, Key=s3key, Fileobj=temp_file
            )
            temp_file.seek(0)
            obj = read_hdf(temp_file.name, **kwargs)

    # npy files
    elif (file_fmt == ".npy") & (obj_class == "numpy"):
        with NamedTemporaryFile() as temp_file:
            s3client.download_fileobj(
                Bucket=bucket, Key=s3key, Fileobj=temp_file
            )
            temp_file.seek(0)
            obj = load(temp_file.name)

    # npz files- This exports each pandas column to a compressed numpy array
    # as a "key-value pair". See numpy documentation for more information
    elif (file_fmt == ".npz") & (obj_class == "numpy"):
        with NamedTemporaryFile() as temp_file:
            s3client.download_fileobj(
                Bucket=bucket, Key=s3key, Fileobj=temp_file
            )
            temp_file.seek(0)
            obj = load(temp_file.name)

    # If none of the above file_fmt and obj_class combination are true. Raise!
    else:
        raise_str = f"""Failed! {file_fmt} export of {obj_class} objects not
            implemented."""
        logger.critical("\tFailed! %s", raise_str)
        raise Exception(raise_str)

    logger.info("\tOK! %s loaded in %0.2f [s]", obj.shape[0], (time() - start))

    return obj


def list_files_in_path(
    bucket,
    prefix,
    drop_sub_folders=True,
    remove_prefix=True,
    subset_ext=None,
    remove_ext=False,
):
    """List all files (sorted) in the specified bucket and prefix.

    Arguments:
        - bucket [str]              - S3 bucket where path i located,
                                      no trailing "/" e.g"stage-data-scientist"
        - prefix [str]              - S3 prefix where files should be listed
        - drop_sub_folders [bool]   - Switch if files in subfolders should
                                      be dropped (default = True)
        - remove_prefix [bool]      - Switch if strings in file_list should
                                      have file prefix removed (default=True)
        - subset_ext [str]          - String ('.csv','.xlsx',...) to subset
                                      file  extension with. If provided
                                      (default=None) file_list will only return
                                      files with the specified file extension.
        - remove_ext [bool]         - Switch if strings in file_list should
                                      have file extension ('.csv','.xlsx',...)
                                      removed (default = False)
    Returns:
        - file_list [lst]           - List of files in bucket-prefix.
    """
    # Initiate Logger
    logger = getLogger(__name__)
    start = time()

    # Remove filename from prefix
    prefix = f"{os.path.dirname(prefix)}/" if prefix != "" else prefix

    logger.info(
        "List files in S3 bucket: bucket = %s, prefix = %s", bucket, prefix
    )

    # List all s3keys
    file_list = [
        objectSummary.key
        for objectSummary in list(
            resource("s3").Bucket(bucket).objects.filter(Prefix=prefix)
        )[0:]
    ]

    file_list = [f for f in file_list if f != prefix]

    # Drop all files in subfolders
    if drop_sub_folders:
        file_list = [
            f
            for f in file_list
            if os.path.dirname(f) == os.path.dirname(prefix)
        ]

    if remove_prefix:
        file_list = [f.replace(prefix, "") for f in file_list]

    # Subset only files ending with provided subset_ext
    if subset_ext:
        file_list = [f for f in file_list if subset_ext in f]

    # Remove all file extensions
    if remove_ext:
        file_list = [os.path.splitext(f)[0] for f in file_list]

    logger.info("\tOK! Elapsed time %f [s]", time() - start)
    return sorted(file_list)


def get_h5_keys(bucket: str, s3key: str):
    """List keys in h5 file located in s3.

    Keyword Arguments:
        - bucket    - S3 export bucket,no trailing "/"
        - s3key     -   S3 export key, no leading "/" String should end with
                        .h5 like "public/.../example.h5"

    """
    s3_filesys = S3FileSystem()
    with s3File(s3_filesys.open("s3://" + bucket + "/" + s3key), "r") as f:
        keys = list(f.keys())

    return keys
