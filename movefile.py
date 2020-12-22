import os   

# ================================ move file and rename to All folder ========================================
numberAll = 0

for j in range(1,6):
    for i in range(1,1001):
        numberAll = numberAll + 1
        old_file_name = 'Data set/New/'+str(j)+'/data'+str(j)+str(i)+'.jpg'
        new_file_name = 'Data set/New/All/data'+str(numberAll)+'.jpg'
        os.rename(old_file_name, new_file_name)
# ====================================================================================================