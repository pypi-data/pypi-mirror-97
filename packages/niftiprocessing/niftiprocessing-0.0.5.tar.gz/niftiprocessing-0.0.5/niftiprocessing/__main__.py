import niftiprocessing
import sys
import os

# Debugging
if __name__ == '__main__':
    test_filepath = os.path.normpath(os.getcwd()).split(os.sep)

    test_filepath = os.path.join(os.sep, *test_filepath[:-1], 'test_directory/004101-1-1.nii.gz')
    # test_filepath = os.path.join(os.sep, *test_filepath[:-1], 'test_directory/test.nii.gz')

    sys.argv = ['niftiproc', test_filepath, '-i', '-a']

    niftiprocessing.main()
