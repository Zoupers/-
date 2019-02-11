# -
云顶书院Python无言组的吴彦组排行榜
# 大致说明

  # 单个网页

  # 排行榜

  def content_handle_and_get_movies():
    get_relative_url()
    get_content(url)
    # 把所有电影块找出来
    # handle block, get useful information(ID一定要注明)
    save_database(*args, **kwargs)


  # 单个电影
  def movie_content_handle_and_get_useful-information():
    # https://movie.douban.com/subject/1292052/
    urls = get_movie_url_from_databse()
    # handle each url
    获取影片详细信息
    save_detail()
    save_actors_url()
    save_photo_url()
    # 处理热评，可能会涉及到用户信息的get


  # 单个电影的演职员cast
  def get_and_handle_actors():
    # https://movie.douban.com/subject/1292052/celebrities
    urls = get_actors_url_from_database()
    # handle each url, 拿下导演，演员，编剧
    save_movie_cose()
    # https://movie.douban.com/celebrity/1054521/
    save_actor_url()
    save_photo_url()


  # 演职员详细信息
  def get_and_handle_actor():
    # https://movie.douban.com/celebrity/1054521/
    urls = get_actor_urls_from_database()
    # handle each url
    save_actor_information()
    save_photo_url()

  class handle_database():
    def __init__():
      pass

    def get_url():
      pass

    def get_content():
      pass
    # ....

