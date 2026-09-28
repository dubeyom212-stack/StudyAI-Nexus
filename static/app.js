// KaTeX receives escaped text, never model-generated HTML; unsafe commands stay disabled.
if (typeof renderMathInElement === 'function') {
  document.querySelectorAll('.preserve, .rubric, .next-step').forEach(element => {
    renderMathInElement(element, {
      delimiters: [
        {left: '$$', right: '$$', display: true},
        {left: '\\[', right: '\\]', display: true},
        {left: '\\(', right: '\\)', display: false},
        {left: '$', right: '$', display: false}
      ],
      throwOnError: false,
      trust: false,
      maxExpand: 100,
      maxSize: 10
    });
  });
}

const search = document.querySelector('#course-search');
if (search) {
  search.addEventListener('input', () => {
    let count = 0;
    document.querySelectorAll('[data-course]').forEach(card => {
      card.hidden = !card.dataset.course.includes(search.value.toLowerCase().trim());
      if (!card.hidden) count++;
    });
    document.querySelector('#course-count').textContent = count ? count + ' courses' : 'No courses found. Try another subject.';
  });
}
document.querySelectorAll('[data-course-select]').forEach(select => {
  select.addEventListener('change', () => {
    const topic = select.form.querySelector('[name="topic"]');
    if (topic) topic.disabled = true;
    select.form.requestSubmit();
  });
});
document.querySelectorAll('form[data-busy]').forEach(form => {
  form.addEventListener('submit', () => {
    form.querySelector('button[type="submit"], button:not([type])').disabled = true;
    form.querySelector('[data-status]').textContent = form.dataset.busy + ' Local AI can take a few minutes. Keep this page open.';
  });
});
