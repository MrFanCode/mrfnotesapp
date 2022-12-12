from app import app,db,User,Notes


with app.app_context():
    user = User.query.all()
    post = Notes.query.all()
    #print(post.author)
    #for post in user.posts:
        #print(post.title)
    #post_1 = Notes(title="Learn", note='Learn to Earn', user_id=user.id)
    #post_2 = Notes(title="Try", note='Try until you lose', user_id=user.id)
    #db.session.add(post_1)
    #db.session.add(post_2)
    #db.session.commit()

