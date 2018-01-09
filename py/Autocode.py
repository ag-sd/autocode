# #start timer
# $elapsed =
#
# $hours = 0
# #Encode for the next $MAX_HOURS hours!
# while ($hours -lt $MAX_HOURS) {
# 	write-host "$hours elapsed so far. Encoding some more..."
# 	# Get next largest file
# 	if (-Not ($file -eq "")) {
# 		# Encode it
#       # Update hours elapsed
# 		$hours = $($elapsed.get_ElapsedMilliseconds()) / 3600000
# 	} else {
# 		#Nothing to process!
# 		#// Simulate the exit condition
# 		$hours = $MAX_HOURS
# 	}
# }
#
# write-host "Ended at $(get-date)"
# write-host "Total Elapsed Time: $($elapsed.Elapsed.ToString())"
#
# Decide-Shutdown of computer

from time import sleep
from datetime import datetime
from utils import database, file
from utils.FileItem import FileItem

MAX_HOURS = 10


def begin_execution(input_dir, output_dir, encoder, max_hours):
    #   Log the start time
    print "Started at " + str(datetime.now())
    hours_elapsed = 0
    process_count = 0

    #   Find all the files that are eligible for encoding
    files_to_process = file.find_files(input_dir)
    print "Found " + str(len(files_to_process)) + " files to process..."

    while len(files_to_process) > 0 and hours_elapsed <= max_hours:
        curr_file = files_to_process.pop()
        print "Evaluating " + str(curr_file)

        #   TODO if encoder.can_process(curr_file)...

        db_file = database.find_file(curr_file)

        if len(db_file) > 1:
            #   More than one file of the same name. Skip
            print str(curr_file) + " has been previously processed! \n Files are:" + str(db_file)

        elif len(db_file) == 1 and db_file[0].file_status == FileItem.FILE_STATUS_COMPLETE:
            print str(curr_file) + " has been previously processed successfully! \n as:" + str(db_file[0])

        else:
            #   1. Start timer
            #   2. Insert/Update entry in the database as started
            #   3. Encode file
            #   4. End timer
            #   5. Update entry in database as complete
            process_count += 1
            # Setup encoding
            start_timer = datetime.now()

            if len(db_file):
                file_to_encode = FileItem(db_file[0].file_name, db_file[0].file_path, db_file[0].file_size)
                file_to_encode.file_status = db_file[0].file_status
                database.update_file(file_to_encode)
                print str(file_to_encode) + " has been previously processed but not successfully! \n " \
                                            "Attempting to re-encode"
            else:
                file_to_encode = FileItem(curr_file.file_name, curr_file.file_path, curr_file.file_size)
                database.insert_file(file_to_encode)
            file_to_encode.set_started(output_dir, file_to_encode.file_name, encoder)
            encode_file(file_to_encode)

            file_to_encode.set_complete()
            database.update_file(file_to_encode)

            td = datetime.now() - start_timer
            mints = (td.total_seconds() / 60)
            hours = mints / 60
            hours_elapsed += hours
            print "File encoded in " + str(mints) + " minutes [ " + str(hours) + " hours]"
            print "Total time taken so far is " + str(hours_elapsed) + " hours"

    print "Encoding completed. Processed " + str(process_count) + " files."

#https://docs.python.org/2/library/subprocess.html#subprocess.Popen
def encode_file(file_item):
    sleep(1)


if __name__ == '__main__':
    begin_execution("/home/sheldon/PycharmProjects/autocode/", "OP", "TEST", 10)
