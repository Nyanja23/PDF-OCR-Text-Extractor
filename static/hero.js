// Smooth scroll helper
    function smoothTo(selector){
      const el = document.querySelector(selector);
      if(!el) return;
      el.scrollIntoView({ behavior: "smooth", block: "start" });
    }

    // Mobile menu toggle
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const navMenu = document.getElementById('navMenu');
    
    mobileMenuBtn.addEventListener('click', () => {
      navMenu.classList.toggle('active');
      mobileMenuBtn.setAttribute('aria-expanded', navMenu.classList.contains('active'));
    });

    // Close mobile menu when clicking outside
    document.addEventListener('click', (e) => {
      if (!navMenu.contains(e.target) && !mobileMenuBtn.contains(e.target) && navMenu.classList.contains('active')) {
        navMenu.classList.remove('active');
        mobileMenuBtn.setAttribute('aria-expanded', 'false');
      }
    });

    // Header scroll effect
    window.addEventListener('scroll', () => {
      const topbar = document.getElementById('topbar');
      if (window.scrollY > 50) {
        topbar.classList.add('scrolled');
      } else {
        topbar.classList.remove('scrolled');
      }
    });

    // Button actions
    document.getElementById("getStartedBtn").addEventListener("click", () => {
      smoothTo(".section:last-of-type");
    });

    document.getElementById("topGetStarted").addEventListener("click", () => {
      smoothTo(".section:last-of-type");
    });

    document.getElementById("finalCta").addEventListener("click", () => {
      alert("Sign up functionality would appear here\nIn production, this would redirect to /signup");
    });

    document.getElementById("watchDemoBtn").addEventListener("click", () => {
      document.getElementById("demoModal").style.display = "flex";
    });

    document.getElementById("closeModal").addEventListener("click", () => {
      document.getElementById("demoModal").style.display = "none";
    });

    document.getElementById("loginTop").addEventListener("click", (e) => {
      e.preventDefault();
      smoothTo("#login");
      alert("Login functionality would appear here\nIn production, this would redirect to /login");
    });

    // Close modal on background click
    document.getElementById("demoModal").addEventListener("click", (e) => {
      if (e.target.id === 'demoModal') {
        e.target.style.display = "none";
      }
    });

    // Close mobile menu when clicking a link
    document.querySelectorAll('.nav-link').forEach(link => {
      link.addEventListener('click', () => {
        navMenu.classList.remove('active');
        mobileMenuBtn.setAttribute('aria-expanded', 'false');
      });
    });

    // Reveal on scroll
    const canAnimate = window.matchMedia("(prefers-reduced-motion: no-preference)").matches;
    if (canAnimate) {
      const io = new IntersectionObserver((entries) => {
        for (const ent of entries) {
          if (ent.isIntersecting) {
            ent.target.classList.add("is-visible");
          }
        }
      }, { threshold: 0.1, rootMargin: "0px 0px -100px 0px" });

      document.querySelectorAll(".reveal").forEach(el => io.observe(el));
    } else {
      document.querySelectorAll(".reveal").forEach(el => el.classList.add("is-visible"));
    }

    // Stats counter animation
    const statElements = document.querySelectorAll('.stat-number');
    const observerOptions = {
      threshold: 0.5,
      rootMargin: '0px 0px -100px 0px'
    };

    const statObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const stat = entry.target;
          const target = parseFloat(stat.textContent);
          let current = 0;
          const increment = target / 30;
          const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
              current = target;
              clearInterval(timer);
            }
            stat.textContent = target % 1 === 0 ? 
              Math.floor(current) : 
              current.toFixed(1);
          }, 40);
          statObserver.unobserve(stat);
        }
      });
    }, observerOptions);

    statElements.forEach(stat => statObserver.observe(stat));

    // Responsive image handling
    window.addEventListener('resize', () => {
      // Close mobile menu on resize to desktop
      if (window.innerWidth > 768) {
        navMenu.classList.remove('active');
        mobileMenuBtn.setAttribute('aria-expanded', 'false');
      }
    });