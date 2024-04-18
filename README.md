# Gaia光谱的下载方式

**注：本教程默认选择下载Gaiadr3的光谱，有需要请根据操作对应下载其他释放版本的光谱即可**

## 一、获取GaiaID的csv文件

### 1. Gaia数据库介绍

​	首先进入Gaia文档，链接：https://gea.esac.esa.int/archive/ 。

<img src="F:\typora\Typora\img\image-20240418182421210.png" alt="image-20240418182421210" style="zoom: 67%;" />

​	点击右上角sign in先进行注册，为了后续可以上传星表。

​	然后点击search，切换到Advanced(ADQL语言)，界面如下图所示：

<img src="F:\typora\Typora\img\image-20240418182542343.png" alt="image-20240418182542343" style="zoom:67%;" />

​	左边的就是Gaia全部的数据，点击加号之后可以看到不同的表，再点击就会出现每个数据有哪些列，点击名称可以查看不同表的描述，并且可以选择展示前20行数据来进行参考。右边的空白地方就是写查询命令的地方，空白处右上角的**Query samples**里面有很多例子。空白处下方是查询结果。

## 2.对自己的星表使用在线交叉匹配来获取Gaia的数据

​	点击下图第一个图标上传用户表，格式请选择csv。

注：请注意，上传csv文件的时候，**Gaia不支持大写英文的文件名**

![image-20240418183103371](F:\typora\Typora\img\image-20240418183103371.png)

​	注意：除了星表中的光谱id，上传的星表中需要包含两个重要的属性列：**ra**和**dec**，ra和dec是用来描述天体位置的坐标系统，其中：

​		ra代表赤经（Right Ascension）

​		dec代表赤纬（Declination）

在上传星表后，勾选表前的空白格，并点击第四个图表来编辑表

<img src="F:\typora\Typora\img\image-20240418183900318.png" alt="image-20240418183900318" style="zoom: 50%;" />

请确认表中的ra和dec，并在其右侧flag下拉框中对应选择"Ra"和"Dec"，之后点击Update更新。

​	之后点击第三个图标进行**交叉匹配**，交叉匹配是在两个不同的天体目录（或数据集）之间进行匹配，并找到在设定的角秒范围内非常接近的天体，**角秒（arcsecond）**是角度的单位，它是角度的1/60分之一，而角度则是用来描述天体位置的测量单位。

​	请参考下图输入用户表和匹配表以及匹配的条件

​	(e.g:限定范围三角秒匹配)

<img src="F:\typora\Typora\img\image-20240418183136208.png" alt="image-20240418183136208" style="zoom:67%;" />

### 3.利用Gaiadr3、用户表和交叉匹配表进行查询

此步骤需要根据需要编写ADQL语句

注：关于ADQL怎么编写，请参考Gaia的官方文档以及右上角的Query example，基本上跟所学的SQL语言一致

请按顺序执行接下来的步骤：

```sql
select id_gaia from gaiadr3.gaia_source as gaia, your_spectrum_table as user_table ,your_crossmatch_table as c where c.gaia_source_source_id=gaia.source_id  and c.tablePrefix_oid = user_table.tablePrefix_oid 
```

然后请点击查询结果右侧第二个图表来上传中间表

![image-20240418191103842](F:\typora\Typora\img\image-20240418191103842.png)

接着执行去重代码：

```sql
select gl.id_gaia from your_update_table as gl,gaiadr3.gaia_source as gaia where gaia.source_id=gl.id_gaia and has_xp_sampled='True' and gl.tablePrefix_oid in (select max(gl2.tablePrefix_oid) from your_update_table as gl2 group by gl2.id_gaia )  
```

请注意：上述代码中很多位置是需要根据你自己上传的表的名称，以及更新到左侧菜单栏的表的名称进行修改的。

补充：本教程只包含了下载Gaia光谱的流程，具体如何下载对应的恒星分类，请参考**Astrophysical parameters**目录下的表，不在此赘述。

### 4.下载结果表

<img src="F:\typora\Typora\img\image-20240418184719615.png" alt="image-20240418184719615" style="zoom: 80%;" />

点击查询结果行右侧第三个图标进行下载即可

其他常用的图标分别是 第二个：将结果表上传至左侧user table中；第五个：展示部分查询结果；第六个：显示ADQL查询语言。



## 二、利用包含GaiaID的csv文件在python上完成光谱数据下载

首先请下载Astroquery库

然后利用download_gaia_csv.py文件下载即可

注：**下载前需要对Astroquery库中的core.py进行修改以支持多进程下载，详见download_gaia_csv.py文件内的注释

