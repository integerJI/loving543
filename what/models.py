from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from who.models import Profile
import re


class Memos(models.Model):
    text = models.TextField(max_length = 150, db_column='내용')
    update_date = models.DateTimeField()
    name = models.ForeignKey(User, on_delete = models.CASCADE,null=True)
    likes = models.ManyToManyField(User, related_name='likes')
    images = models.ImageField(blank=True, upload_to="usr", null=True)
    secret = models.BooleanField(db_column='나만보기', null=True, blank=True)
    tag_set = models.ManyToManyField('Tag', blank=True)
    text2 = models.TextField(max_length = 150, null=True)
    tag_set2 = models.ManyToManyField('Tag2', blank=True)
    text3 = models.TextField(max_length = 150, null=True)


    # NOTE: content에서 tags를 추출하여, Tag 객체 가져오기, 신규 태그는 Tag instance 생성, 본인의 tag_set에 등록,
    def tag_save(self):
        tags = re.findall(r'#(\w+)\b', self.text)

        if not tags:
            return

        for t in tags:
            tag, tag_created = Tag.objects.get_or_create(tag_name=t)
            self.tag_set.add(tag)  # NOTE: ManyToManyField 에 인스턴스 추가

    # NOTE: content에서 tags를 추출하여, Tag 객체 가져오기, 신규 태그는 Tag instance 생성, 본인의 tag_set에 등록,
    def tag_save2(self):
        tags2 = re.findall(r'#(\w+)\b', self.text3)

        if not tags2:
            return

        for t2 in tags2:
            tag2, tag_created2 = Tag2.objects.get_or_create(tag_name2=t2)
            self.tag_set2.add(tag2)  # NOTE: ManyToManyField 에 인스턴스 추가
            
    def generate(self):
        self.update_date = timezone.now()
        self.save()

    def __str__(self):
        return self.text2
        
    @property
    def total_likes(self):
        return self.likes.count()

class Comment(models.Model):
    post = models.ForeignKey(Memos, on_delete=models.CASCADE, null=True, related_name='comments')
    comment_date = models.DateTimeField(auto_now_add=True)
    comment_contents = models.CharField(max_length=200)
    comment_writer = models.ForeignKey(Profile, on_delete=models.CASCADE, null = True)

    class Meta:
        ordering = ['-id']
            
    def __str__(self):
        return str(self.comment_writer)


class Tag(models.Model):
    tag_name = models.CharField(max_length=140, unique=True)

    def __str__(self):
        return self.tag_name

class Tag2(models.Model):
    tag_name2 = models.CharField(max_length=140, unique=True)

    def __str__(self):
        return self.tag_name2