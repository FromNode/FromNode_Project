DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'fromnode', 
        'USER': 'admin',
        'PASSWORD': 'ohylab123',
        'HOST': 'db-fromnode.c0cxgccf3tyi.ap-northeast-2.rds.amazonaws.com',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            # 'sql_mode': 'traditional',
        },
    }
}