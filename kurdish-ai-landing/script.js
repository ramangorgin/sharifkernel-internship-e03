(() => {
  'use strict';

  const hidePreloader = () => {
    const preloader = document.getElementById('preloader');
    if (!preloader) return;
    preloader.classList.add('is-hidden');
    window.setTimeout(() => preloader.remove(), 650);
  };

  const initializePage = () => {
    const year = document.getElementById('year');
    if (year) year.textContent = new Date().getFullYear();

    if (window.lucide && typeof window.lucide.createIcons === 'function') {
      window.lucide.createIcons();
    }

    const menuToggle = document.getElementById('menu-toggle');
    const navigation = document.getElementById('primary-nav');

    if (menuToggle && navigation) {
      const closeMenu = () => {
        navigation.classList.remove('is-open');
        menuToggle.setAttribute('aria-expanded', 'false');
        menuToggle.setAttribute('aria-label', 'Open navigation');
        menuToggle.innerHTML = '<i data-lucide="menu"></i>';
        if (window.lucide) window.lucide.createIcons();
      };

      menuToggle.addEventListener('click', () => {
        const isOpen = navigation.classList.toggle('is-open');
        menuToggle.setAttribute('aria-expanded', String(isOpen));
        menuToggle.setAttribute('aria-label', isOpen ? 'Close navigation' : 'Open navigation');
        menuToggle.innerHTML = isOpen ? '<i data-lucide="x"></i>' : '<i data-lucide="menu"></i>';
        if (window.lucide) window.lucide.createIcons();
      });

      navigation.querySelectorAll('a').forEach((link) => {
        link.addEventListener('click', closeMenu);
      });

      document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape') closeMenu();
      });

      document.addEventListener('click', (event) => {
        if (!navigation.contains(event.target) && !menuToggle.contains(event.target)) closeMenu();
      });
    }

    const revealElements = document.querySelectorAll('.feature-card, .tech-item, .roadmap-step, .insight-strip, .intro-grid, .section-heading');
    revealElements.forEach((element) => element.classList.add('reveal-ready'));

    if ('IntersectionObserver' in window) {
      const observer = new IntersectionObserver((entries, currentObserver) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            currentObserver.unobserve(entry.target);
          }
        });
      }, { threshold: 0.12, rootMargin: '0px 0px -35px 0px' });
      revealElements.forEach((element) => observer.observe(element));
    } else {
      revealElements.forEach((element) => element.classList.add('is-visible'));
    }

    // Hide the loader after the page has had a moment to render.
    window.setTimeout(hidePreloader, 350);
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializePage, { once: true });
  } else {
    initializePage();
  }

  // Fallback in case a third-party resource delays the normal initialization.
  window.addEventListener('load', hidePreloader, { once: true });
  window.setTimeout(hidePreloader, 5000);
})();
