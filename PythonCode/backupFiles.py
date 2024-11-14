import os

# 源目录
src_pub_path = r'D:\public'
# 目标目录
target_pub_path = r'E:\BackUpFiles\public'

src_prv_path = r'D:\private'
# 目标目录
target_prv_path = r'E:\BackUpFiles\private'


src_git_path = r'D:\Git'
# 目标目录
target_git_path = r'E:\BackUpFiles\Git'

src_svn_path = r'D:\SVN'
# 目标目录
target_svn_path = r'E:\BackUpFiles\SVN'


src_xpp_path = r'D:\xampp'
# 目标目录
target_xpp_path = r'E:\BackUpFiles\xampp'


def copy(src_path, target_path):
	# 源目录的文件名，保存到列表中
    file_list = os.listdir(src_path)
    # 判断目录是否在
    if os.path.exists(src_path) and os.path.exists(target_path):
		# 遍历 源目录下的文件名列表
        for file in file_list:
        	# 拼接源目录文件path
            path = os.path.join(src_path, file)
            # 判断文件是文件夹还是文件，如果是文件夹需要新建文件夹path
            if os.path.isdir(path):
				# 拼接目标文件的path
                target_path1 = os.path.join(target_path, file)
				# 判断目标文件夹目录是否存在
                if os.path.exists(target_path1):
					# 文件夹存在，直接递归调用
                    copy(path, target_path1)

                else:
                	# 文件夹不存在
                    # 新建文件夹，再递归调用copy

                    os.mkdir(target_path1)
                    copy(path, target_path1)

            else:
            	# 复制文件
                with open(path, 'rb') as stream_r:
                    container = stream_r.read()
                    path1 = os.path.join(target_path, file)
                    with open(path1, 'wb') as stream_w:
                        stream_w.write(container)


        else:
            print("复制完成  ", target_path)
    elif os.path.exists(target_path) == False:
        print("目标目录不存在")
    elif os.path.exists(src_path) == False:
        print("源文件目录不存在")



copy(src_pub_path, target_pub_path)

copy(src_prv_path, target_prv_path)

copy(src_git_path, target_git_path)

copy(src_svn_path, target_svn_path)

copy(src_xpp_path, target_xpp_path)
      




