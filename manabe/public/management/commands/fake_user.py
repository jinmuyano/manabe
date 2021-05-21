from django.contrib.auth.models import User,Group

def fake_user_data():
    User.objects.all().delete()   #清除所有用户
    Group.objects.all().delete()   #清除所有用户组
    print("delete all user data")
    User.objects.create_user(username='Dylan', password="password")
    User.objects.create_user(username='Tyler', password="password")
    User.objects.create_user(username='Kyle', password="password")
    User.objects.create_user(username='Dakota', password="password")
    User.objects.create_user(username='Marcus', password="password")
    User.objects.create_user(username='Samantha', password="password")
    User.objects.create_user(username='Kayla', password="password")
    User.objects.create_user(username='Sydney', password="password")
    User.objects.create_user(username='Courtney', password="password")
    User.objects.create_user(username='Mariah', password="password")
    User.objects.create_user(username='tom', password="password")
    User.objects.create_user(username='mary', password="password")
    admin = User.objects.create_superuser('admin','admin@demon.com','admin')   #创建超级用户
    root = User.objects.create_superuser('root','root@demon.com','root')     #创建超级用户
    admin_group=Group.objects.create(name='admin')      #创建一个admin用户组
    Group.objects.create(name='test')      #建立3个用户组
    Group.objects.create(name='dev')
    Group.objects.create(name='operate')
    admin_users=[admin,root]
    admin_group.user_set.set(admin_users)   #将2个超级用户加入admin组
    print('create all user data')