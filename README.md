# qiniu-js-upload
学习用JavaScript做七牛云上传的时候写的一个demo，由于自己在这里掉了很多坑，而且七牛的官方文档又是烂到爆，所以想写下来。
注意：只适合新手使用

## 参数设置

七牛的官方demo使用的是plupload插件来做上传的，确实很好用，但是demo解释的太差劲。
在页面中引入plupload.js 、qiniu.js后，会有下面一堆：
```javascript
	var uploader = Qiniu.uploader({
        runtimes: 'html5,flash,html4', //上传模式,依次退化
        browse_button: 'pickfiles', //上传选择的点选按钮，**必需**

        uptoken_url: '/token', //Ajax请求upToken的Url，**强烈建议设置**（服务端提供）
        // uptoken: "", //若未指定uptoken_url,则必须指定 uptoken ,uptoken由其他程序生成
        // unique_names: true, // 默认 false，key为文件名。若开启该选项，SDK为自动生成上传成功后的key（文件名）。
        save_key: true, // 默认 false。若在服务端生成uptoken的上传策略中指定了 `sava_key`，则开启，SDK会忽略对key的处理

        domain: 'http://YOUR_BUCKET.qiniudn.com/', //bucket 域名，下载资源时用到，**必需**

        get_new_uptoken: false, //设置上传文件的时候是否每次都重新获取新的token
        container: 'container', //上传区域DOM ID，默认是browser_button的父元素，
        max_file_size: '100mb', //最大文件体积限制
        flash_swf_url: '../libs/plupload/Moxie.swf', //引入flash,相对路径
        silverlight_xap_url: '../libs/plupload/Moxie.xap',
        max_retries: 1, //上传失败最大重试次数
        dragdrop: true, //开启可拖曳上传
        drop_element: 'droparea', //拖曳上传区域元素的ID，拖曳文件或文件夹后可触发上传
        chunk_size: '4mb', //分块上传时，每片的体积
        auto_start: true,
        init:{}
    })
```

其实我们只需要关注几个参数：

1. `uptoken_url`和`uptoken`:这两个参数选其中一个。`uptoken_url`是Ajax GET获取`uptoken`的地址，返回的格式必须是如下，而uptoken是直接又后台程序填充的字符串:
```javascript
{
	"uptoken":"...THE＿TOKEN..."
}
```
2. 在后台生成`uptoken`时,以指定上传后文件的名字`key`（用于替换文件），也可以不指定文件的名字，而是使用`policy`参数中`saveKey`字段来设置上传后名字的格式，如下：
```python
# 后台生成uptoken时设置policy中的saveKey参数
policy = {"saveKey": "$(year)$(mon)$(day)_$(hour)$(min)$(sec)_$(fname)"}
```
比如选择上传的文件名为`foo.jpg`，上传后就变成了`20160811_154032_foo.jpg`

3. 基于上一条，设置js中的 `unique_names`和`save_key`。
```javascript
// 服务器既没有指定key,也没有指定saveKey时:
// init.Key函数被屏蔽
	unique_names:true, 
	save_key: false

// 服务器只指定saveKey,没有指定key时:
// init.Key函数被屏蔽
	unique_names: false,  
	save_key: true

// 服务器只指定key,没有指定saveKey时:
// 此时需要设置init.Key函数，返回值为服务器端设置的key值
	unique_names: false, 
	save_key: false


```
设置init.Key函数：
```javascript
var uploader = Qiniu.uploader({
		uptoken_url: '/token', //Ajax请求upToken的Url，**强烈建议设置**（服务端提供）
        unique_names: false, 
        save_key: false, 
        ...
        init:{
        	"Key":function(up, file){
        		key = 'your_key';
        		return key;
        	}
        }
    })

```

4. 最后根据自己的情况设置 `browse_button`,`domain`,`container`,`flash_swf_url`,`silverlight_xap_url`,`drop_element`,`auto_start`,以及`init`中的各个函数就可以上传了

