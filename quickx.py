#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Author: lonewolf
# Date: 2013-10-26 11:23:48
# 
# add cocos2d-x api generator @terran 2015-12-15
# 
import sublime
import sublime_plugin
import functools
import os
import datetime
import json
import re
import subprocess
import sys
import time
import codecs
try:
    import helper
    import rebuild
except ImportError:
    from . import helper
    from . import rebuild

try:
    import cocos2dxSnippet
except ImportError:
    from . import cocos2dxSnippet   

TEMP_PATH="" 
# [wordsArr,showFunc,path,lineNum,type] type=0 user, 1 lua, 2 cocos2dx
USER_DEFINITION_LIST=[]
luaTemplate="""--
-- Author: ${author}
-- Date: ${date}
--
"""

# init plugin,load definitions
def init():
    global TEMP_PATH
    TEMP_PATH=sublime.packages_path()+"/User/QuickXDev.cache"
    global USER_DEFINITION_LIST
    path=os.path.join(TEMP_PATH,"user_definition.json")
    if os.path.exists(path):
        USER_DEFINITION_LIST=json.loads(helper.readFile(path))
    

class LuaNewFileCommand(sublime_plugin.WindowCommand):
    def run(self, dirs):
        self.window.run_command("hide_panel")
        title = "untitle"
        on_done = functools.partial(self.on_done, dirs[0])
        v = self.window.show_input_panel(
            "File Name:", title + ".lua", on_done, None, None)
        v.sel().clear()
        v.sel().add(sublime.Region(0, len(title)))

    def on_done(self, path, name):
        filePath = os.path.join(path, name)
        if os.path.exists(filePath):
            sublime.error_message("Unable to create file, file exists.")
        else:
            code = luaTemplate
            # add attribute
            settings = helper.loadSettings("QuickXDev")
            format = settings.get("date_format", "%Y-%m-%d %H:%M:%S")
            date = datetime.datetime.now().strftime(format)
            code = code.replace("${date}", date)
            author=settings.get("author", "Your Name")
            code = code.replace("${author}", author)
            # save
            helper.writeFile(filePath, code)
            v=sublime.active_window().open_file(filePath)
            # cursor
            v.run_command("insert_snippet",{"contents":code})
            sublime.status_message("Lua file create success!")

    def is_enabled(self, dirs):
        return len(dirs) == 1


class QuickxGotoDefinitionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # select text
        sel=self.view.substr(self.view.sel()[0])
        if len(sel)==0:
            # extend to the `word` under cursor
            sel=self.view.substr(self.view.word(self.view.sel()[0]))
        # find all match file
        matchList=[]
        showList=[]

        for item in USER_DEFINITION_LIST:
            if len(item)!=5:
                continue
            for key in item[0]:
                if key==sel:
                    matchList.append(item)
                    showList.append(item[1])
        if len(matchList)==0:
            sublime.status_message("Can not find definition '%s'"%(sel))
        elif len(matchList)==1:
            self.gotoDefinition(matchList[0])
        else:
            # multi match
            self.matchList=matchList
            on_done = functools.partial(self.on_done)
            self.view.window().show_quick_panel(showList,on_done)
        
    def on_done(self,index):
        if index==-1:
            return
        item=self.matchList[index]
        self.gotoDefinition(item)
    
    def gotoDefinition(self,item):
        definitionType=item[4]
        filepath=item[2]
        if os.path.exists(filepath):
            self.view.window().open_file(filepath+":"+str(item[3]),sublime.ENCODED_POSITION)
        else:
            sublime.status_message("%s not exists"%(filepath))

    def is_enabled(self):
        return helper.checkFileExt(self.view.file_name(),"lua")

    def is_visible(self):
        return self.is_enabled()


class QuickxRebuildUserDefinitionCommand(sublime_plugin.WindowCommand):
    def __init__(self,window):
        super(QuickxRebuildUserDefinitionCommand,self).__init__(window)
        self.lastTime=0

    def run(self, dirs):
        curTime=time.time()
        if curTime-self.lastTime<3:
            sublime.status_message("Rebuild frequently!")
            return
        self.lastTime=curTime
        global USER_DEFINITION_LIST
        USER_DEFINITION_LIST=rebuild.rebuild(dirs[0],TEMP_PATH)
        path=os.path.join(TEMP_PATH, "user_definition.json")
        data=json.dumps(USER_DEFINITION_LIST)
        if not os.path.exists(TEMP_PATH):
            os.makedirs(TEMP_PATH)
        helper.writeFile(path,data)
        sublime.status_message("Rebuild user definition complete!")
    
    def is_enabled(self, dirs):
        return len(dirs)==1

    def is_visible(self, dirs):
        return self.is_enabled(dirs)

class QuickxRebuildCocos2dxApiCommand(sublime_plugin.WindowCommand):
    def __init__(self,window):
        super(QuickxRebuildCocos2dxApiCommand,self).__init__(window)
        self.lastTime=0

    def run(self, dirs):
        curTime=time.time()
        if curTime-self.lastTime<3:
            sublime.status_message("Rebuild frequently!")
            return
        self.lastTime=curTime

        cocos2dxSnippet.run(dirs[0],TEMP_PATH);
        sublime.status_message("Rebuild user definition complete!")
    
    def is_enabled(self, dirs):
        return len(dirs)==1

    def is_visible(self, dirs):
        return self.is_enabled(dirs) and os.path.basename(dirs[0]) == "frameworks"

# build file definition when save file
class QuickxListener(sublime_plugin.EventListener):
    def __init__(self):
        self.lastTime=0

    def on_post_save(self, view):
        filename=view.file_name()
        if not filename:
            return
        if not helper.checkFileExt(filename,"lua"):
            return
        # rebuild user definition
        curTime=time.time()
        if curTime-self.lastTime<2:
            return
        self.lastTime=curTime
        a=rebuild.rebuildSingle(filename,TEMP_PATH)
        arr=a[0]
        path=a[1] 
        # remove prev
        global USER_DEFINITION_LIST
        for i in range(len(USER_DEFINITION_LIST)-1,0,-1):
            item=USER_DEFINITION_LIST[i]
            if item[2]==path:
                USER_DEFINITION_LIST.remove(item)
        USER_DEFINITION_LIST.extend(arr)
        path=os.path.join(TEMP_PATH, "user_definition.json")
        data=json.dumps(USER_DEFINITION_LIST)
        if not os.path.exists(TEMP_PATH):
            os.makedirs(TEMP_PATH)
        helper.writeFile(path,data)
        sublime.status_message("Current file definition rebuild complete!")

# st3
def plugin_loaded():
    sublime.set_timeout(init, 200)

# st2
if not helper.isST3():
    init()

