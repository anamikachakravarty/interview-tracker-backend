from django.db import models

class LearningTopic(models.Model):

    class TopicStatus(models.TextChoices):
        NEW = 'New', 'New Topic'
        IN_PROGRESS = 'In Progress', 'In Progress'
        DONE = 'Done', 'Done'

    class TopicPriority(models.TextChoices):
        LOW = 'Low', 'Low'
        MEDIUM = 'Medium', 'Medium'
        HIGH = 'High', 'High'

    title = models.CharField(max_length=150)

    description = models.TextField(blank=True)

    category = models.CharField(max_length=80)

    priority = models.CharField(
        max_length=20,
        choices=TopicPriority.choices,
        default=TopicPriority.MEDIUM
    )

    status = models.CharField(
        max_length=20,
        choices=TopicStatus.choices,
        default=TopicStatus.NEW
    )

    start_date = models.DateField(blank=True, null=True)

    target_date = models.DateField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class LearningModule(models.Model):

    topic = models.ForeignKey(
        LearningTopic,
        on_delete=models.CASCADE,
        related_name='modules'
    )

    title = models.CharField(max_length=150)

    description = models.TextField(blank=True)

    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    position = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.topic.title} - {self.title}"

class LearningMilestone(models.Model):

    module = models.ForeignKey(
        LearningModule,
        on_delete=models.CASCADE,
        related_name='milestones'
    )

    title = models.CharField(max_length=150)

    description = models.TextField(blank=True)

    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    is_completed = models.BooleanField(default=False)

    completed_at = models.DateTimeField(
        blank=True,
        null=True
    )

    position = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.module.title} - {self.title}"

class LearningResource(models.Model):

    class ResourceType(models.TextChoices):
        VIDEO = 'Video', 'Video'
        ARTICLE = 'Article', 'Article'
        COURSE = 'Course', 'Course'
        DOCUMENTATION = 'Documentation', 'Documentation'
        PRACTICE = 'Practice', 'Practice'
        OTHER = 'Other', 'Other'

    topic = models.ForeignKey(
        LearningTopic,
        on_delete=models.CASCADE,
        related_name='resources',
        blank=True,
        null=True
    )

    module = models.ForeignKey(
        LearningModule,
        on_delete=models.CASCADE,
        related_name='resources',
        blank=True,
        null=True
    )

    title = models.CharField(max_length=200)

    url = models.URLField()

    resource_type = models.CharField(
        max_length=30,
        choices=ResourceType.choices,
        default=ResourceType.OTHER
    )

    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(topic__isnull=False, module__isnull=True)
                    | models.Q(topic__isnull=True, module__isnull=False)
                ),
                name='resource_belongs_to_topic_or_module'
            )
        ]

    def __str__(self):
            return self.title

class LearningNote(models.Model):

    topic = models.OneToOneField(
        LearningTopic,
        on_delete=models.CASCADE,
        related_name='notes'
    )

    content = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Notes - {self.topic.title}"

class LearningRevision(models.Model):

    class RevisionStatus(models.TextChoices):
        PENDING = 'Pending', 'Pending'
        COMPLETED = 'Completed', 'Completed'
        SKIPPED = 'Skipped', 'Skipped'

    milestone = models.ForeignKey(
        LearningMilestone,
        on_delete=models.CASCADE,
        related_name='revisions'
    )

    scheduled_date = models.DateField()

    revision_number = models.PositiveIntegerField()

    status = models.CharField(
        max_length=20,
        choices=RevisionStatus.choices,
        default=RevisionStatus.PENDING
    )

    completed_at = models.DateTimeField(
        blank=True,
        null=True
    )

    revision_notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['scheduled_date', 'revision_number']

    def __str__(self):
        return (
            f"Revision {self.revision_number} - "
            f"{self.milestone.title}"
        )