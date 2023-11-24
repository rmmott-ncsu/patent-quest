#makeWordCloud.py

def visualizeWordCloud(sorted_tokens, stop_words, make_wordcloud_jpg, wordcloud_filename):
                                           
    import numpy as np
    from wordcloud import WordCloud
    from PIL import Image
    import matplotlib.pyplot as plt
    
    ###############################################################################
    #create word cloud
    ###############################################################################
    
    # for p in sorted_tokens.keys():
    #     sorted_tokens[p]=0
    #     for q in response_query:
    #         if p in q:
    #             sorted_tokens[p] = sorted_tokens[p]+1
    
    word_cloud_mat = []
    
    for k in sorted_tokens.keys():
        k_space = k + ' '
        word_cloud_mat = word_cloud_mat + ([k_space])*sorted_tokens[k]
    
    word_cloud_str = np.array(word_cloud_mat)
    np.random.shuffle(word_cloud_str)
    word_cloud_str = ''.join(word_cloud_str)
    
    # mask = np.array(Image.open("ny_mono.jpg"))
    
    wordcloud = WordCloud(width = 800, height = 800,
                    background_color ='white',
                    stopwords = stop_words,
                    min_font_size = 8).generate(word_cloud_str)
    
    plt.figure(figsize = (8, 8), facecolor = None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad = 0)
     
    plt.show()
    if make_wordcloud_jpg == 'True':
        wordcloud.to_file(wordcloud_filename + ".jpg")