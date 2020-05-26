# wsvd_dataset_loader
Loader for the WSVD dataset - eliminating invalid/deleted youtube videos or the videos with copyright issues.

## Web Stereo Video Supervision for Depth Prediction from Dynamic Scenes
For more details, please see the paper [Wang etal. 3DV19](https://arxiv.org/pdf/1904.11112.pdf)
<br>
<br>
Please also see the original website https://sites.google.com/view/wsvd/home, and the original repository of the authors https://github.com/MightyChaos/wsvd_test
<br>
<br>
To download the dataset, you can directly run the following script, which will create a subdirectory wsvd inside your working folder, and directly start downloading the videos in the dataset. The dataset is approximately 50G.
<code>bash downloader_script.sh</code>
<br>
<br>
If you would like to generate the video ID list again, you will need a YouTube API key. In that case, create your YouTube API key, and fill it in the script <code>valid_id_list_creator.py</code>
