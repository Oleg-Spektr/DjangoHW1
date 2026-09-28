from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from blog.models import BlogEntry

# 1. READ (Список статей) с фильтрацией опубликованных
class BlogListView(ListView):
    model = BlogEntry
    template_name = 'blog/blog_list.html'
    context_object_name = 'blogs'

    # Критерий: выводим только статьи с положительным признаком публикации
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)

# 2. READ (Детальный просмотр) с увеличением счетчика просмотров
class BlogDetailView(DetailView):
    model = BlogEntry
    template_name = 'blog/blog_detail.html'
    context_object_name = 'blog'

    # Критерий: при открытии статьи увеличиваем счетчик просмотров
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save()
        return obj

# 3. CREATE (Создание статьи)
class BlogCreateView(CreateView):
    model = BlogEntry
    fields = ('title', 'content', 'preview', 'is_published')
    template_name = 'blog/blog_form.html'
    success_url = reverse_lazy('blog:list')

# 4. UPDATE (Редактирование статьи) с динамическим перенаправлением
class BlogUpdateView(UpdateView):
    model = BlogEntry
    fields = ('title', 'content', 'preview', 'is_published')
    template_name = 'blog/blog_form.html'

    # Критерий: после успешного редактирования перенаправляем на просмотр ЭТОЙ статьи
    def get_success_url(self):
        return reverse('blog:detail', kwargs={'pk': self.object.pk})

# 5. DELETE (Удаление статьи)
class BlogDeleteView(DeleteView):
    model = BlogEntry
    template_name = 'blog/blog_confirm_delete.html'
    success_url = reverse_lazy('blog:list')
