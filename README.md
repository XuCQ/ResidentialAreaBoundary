# 小区边界爬取

1. 数据源：[百度地图api](https://lbsyun.baidu.com/index.php?title=jspopular/guide/introduction)
2. RESIDENTIALAREABOUNDARY

   │  ResidentialAreaBoundaryControl.py 主函数
   
   │  ResidentialAreaBoundaryFunc.py 方法库
   
   ├─Auxiliary
   
   │  │  crawelFunc.py 辅助函数
   
   └─data
   
           czfjsj.csv 样例-小区数据
           
           czfjsj_boundary.csv 样例-小区边界爬取结果
           
3. 主函数需要参数：
   - orgin_csv_path：小区数据csv（参考 czfjsj.csv，仅需小区名称和位置即可）
   - output_path：输出目录
   - bd_ak：[百度地图ak列表](http://lbsyun.baidu.com/apiconsole/key?application=key)，建议数据量大多添加几个ak，防止配额用完，该版本并未添加配额监测、负载均衡、断点续存等功能
