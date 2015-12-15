Base on QuickXDev  --ver 3.3
=========

Powerful cocos2d-x develop plugin for sublime text 2/3

CHINESE：<a href="http://my.oschina.net/lonewolf/blog?catalog=412647" target="_blank">http://my.oschina.net/lonewolf/blog?catalog=412647</a>

## Description

A quick-cocos2d-x develop plugin for sublime text 2/3.

##Features

 * cocos2d-x api completions support
 * goto definition
 * user definition auto completion
 * system api completions support (lua 5.1)
 * some snippets,like if-else,if-elseif-else,while,comment,repeat-until....
 * create new lua file with template
 * lua biuld system

## Installation


1.Download .zip source file, then unzip it,rename it with "QuickXDev",then clone "QuickXDev" folder into the SublimeText ```Packages``` directory.  A restart of SublimeText might be nessecary to complete the install.


## Usage

###setting

```
{
    "author": "<your name>",
}
```

### User definition auto completion

 right click "src" folder on the sidebar,select "Rebuild User Definition".
 and when you save a lua file in sublime,it will auto build all user definition in the current file.

### Cocos2dx lua api generation
 right click "frameworks" folder on the sidebar,select "Rebuild cocos2dx api".