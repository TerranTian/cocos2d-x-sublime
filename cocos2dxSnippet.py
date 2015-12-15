#coding=utf-8
import os
import re
import shutil
try:
    import helper
except ImportError:
    from . import helper



#the out snippet path,you may copy them to sublime package directory yourself
output_path = "cocos2dx_snippet/"

#snippet format
format_text = '<snippet>\n\t<content><![CDATA[%s]]></content>\n\t<tabTrigger>%s</tabTrigger>\n\t<scope>source.lua</scope>\n\t<description>%s</description>\n</snippet>'

#deal with className
def dealWithModule(className, readfp, parent_path):
	file_name = parent_path + "/" + className + ".sublime-snippet"
	module_name = ''
	while len(readfp)>0:
		line_text = readfp.pop(0);
		result = re.match(r'.*@parent_module (\w+)', line_text)
		if result:
			module_name = result.group(1)
			break
	if module_name != "":
		trigger_text = className
		content_text = module_name + "." + className
		outfp = open(file_name, "w")
		write_text = format_text %(content_text, trigger_text, ".")
		outfp.write(write_text)
		outfp.close()
	
#deal with create function
def dealWithCreate(className, readfp, parent_path):
	#get params
	#show longest param,ignore shorter
	param_list = []

	while len(readfp)>0:
		line_text = readfp.pop(0);
		result = re.match(r'.*@return .*', line_text)
		if result:
			break
		else:
			result = re.match(r'.*@param .* (\w+)', line_text)
			if result:
				param_list.append(result.group(1))
	
	#trigger add className and param num, ignore param name to make it can be found easier
	trigger_text = "create_%s_%d" %(className.lower(), len(param_list))
	content_text = "create("	
	for i in range(0, len(param_list)):
		param_name = param_list[i]
		if i > 0:
			content_text = content_text + ', '
		tmp_text = '${%d:%s}' %(i+1, param_name)
		content_text = content_text + tmp_text

	content_text = content_text + ')'
	file_name = parent_path + "/create.sublime-snippet"
	outfp = open(file_name, "w")
	write_text = format_text %(content_text, trigger_text, className)  #description show className
	outfp.write(write_text)
	outfp.close()

#deal with common function	
def dealWithFunction(funcName, readfp, parent_path, className):
	#get param list
	#just show longest param,ignore shorter
	param_list = []
	
	while len(readfp)>0:
		line_text = readfp.pop(0);
		result = re.match(r'.*@return .*', line_text)
		if result:
			break
		else:
			result = re.match(r'.*@param .* (\w+)', line_text)
			if result:
				param_list.append(result.group(1))
	
	trigger_text = funcName + '('
	content_text = trigger_text	
	for i in range(0, len(param_list)):
		param_name = param_list[i]
		if i > 0:
			trigger_text = trigger_text + ', ' 
			content_text = content_text + ', '
		trigger_text = trigger_text + param_name
		tmp_text = '${%d:%s}' %(i+1, param_name)  #for tab key
		content_text = content_text + tmp_text
		
	trigger_text = trigger_text + ')'
	content_text = content_text + ')'
	file_name = parent_path + "/" + funcName + ".sublime-snippet"  #snippet file
	outfp = open(file_name, "w")
	write_text = format_text %(content_text, trigger_text, className)  #description show className
	outfp.write(write_text)
	outfp.close()

#deal one api file			
def dealWithFile(filepath):
	#get filename to mkdir
	base_name = os.path.basename(filepath)
	base_name = os.path.splitext(base_name)[0]
	parent_path = os.path.abspath(os.path.join(output_path,base_name))
	os.mkdir(parent_path)
	
	readfp = helper.readFile(filepath).splitlines()
	
	while len(readfp)>0:
		line_text = readfp.pop(0);
		#first match className
		result = re.match(r'.*@module (\w+)', line_text)
		if result:
			className = result.group(1)
			dealWithModule(className, readfp, parent_path)
		else:
			#match function
			result = re.match(r'.*@function .* (\w+)', line_text)
			if result:
				funcName = result.group(1)
				#too many function named create,deal it single
				if funcName == "create":
					dealWithCreate(className, readfp, parent_path)
				elif funcName != className:         #ignore constructor
					dealWithFunction(funcName, readfp, parent_path, className)

def run(path,outpath):
	global output_path;
	output_path = os.path.join(outpath,"cocos2dx_snippet");
	if(os.path.exists(output_path)): shutil.rmtree(output_path,True);
	os.mkdir(output_path)

	apis = helper.getFileList(path,"*/api/*.lua","*/lua_cocos2dx_*.lua");
	for api in apis:
		# print(api);
		dealWithFile(api)
	# pass
	
# run("/Users/terrantian/Documents/wukong_workspace/wukong_client/trunk/mk/frameworks",".")

	
# def main():
# 	#remove old snippet
# 	if os.path.isdir(output_path):
# 		shutil.rmtree(output_path)
# 	os.mkdir(output_path)
	
# 	#deal with api file
# 	if not os.path.isdir(api_path):
# 		print "Please change cocos2dx_root and output_path to your path."
# 		return
# 	for file in os.listdir(api_path):
# 		#ignore .DStore and lua_cocos2dx_...
# 		if file[0] != "." and not file.startswith("lua_cocos2dx") :
# 			dealWithFile(api_path + file)

# if __name__ == '__main__':
# 	main()