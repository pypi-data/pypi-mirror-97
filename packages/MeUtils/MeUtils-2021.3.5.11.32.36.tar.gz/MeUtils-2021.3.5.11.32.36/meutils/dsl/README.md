1. 在conf文件夹下添加push_mitv_conf相关配置
2. 修改CMakeLists.txt
    ```
    # Install Conf files
    set(INSTALL_CONF_NAME_LIST
        conf/ctr_score_conf
        conf/gr_conf
        conf/inlinevideo_tf_serving
        conf/inlinevideo_completeness
        conf/news_dwelltime
        conf/fastvideo
        conf/ctr_inlinevideo_conf
        conf/recall_conf
        conf/rough_inlinevideo_conf
        conf/ottvideo
        conf/rubrowser
        conf/rumivideo
        conf/related_conf
        conf/mini_video_ctr_score_conf
        conf/zili
        conf/ottminivideo
        conf/edge_rec_conf
        conf/mishop_push_conf
        conf/zili_push_conf
        conf/push
    )
    ```
3. 获取libfeature.so
```
./release.sh && hdfs dfs -put ./build/libfeature.so /user/s_feeds/yuanjie/dsl # /newname.so
```

4. debug samples
TODO: 转DF
```
print(
    s.replace('GroupedFeature', '\nGroupedFeature')
    .replace('features', '\n\tfeatures')
    .replace('BaseFeature', '\n\t\tBaseFeature')
)

```