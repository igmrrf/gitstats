
// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
  // Set current year in the footer
  document.getElementById('current-year').textContent = new Date().getFullYear();
  
  // Initialize mobile menu toggle
  initMobileMenu();
  
  // Initialize navbar scroll effect
  initNavbarScroll();
  
  // Initialize smooth scrolling for anchor links
  initSmoothScroll();
  
  // Initialize the animated logo
  initAnimatedLogo();
  
  // Initialize intersection observers for animations
  initIntersectionObservers();
  
  // Initialize charts
  initCharts();
});

// Mobile menu toggle
function initMobileMenu() {
  const mobileToggle = document.getElementById('mobile-toggle');
  const mobileMenu = document.getElementById('mobile-menu');
  const menuIcon = document.getElementById('menu-icon');
  const closeIcon = document.getElementById('close-icon');
  
  mobileToggle.addEventListener('click', function() {
    mobileMenu.classList.toggle('hidden');
    menuIcon.classList.toggle('hidden');
    closeIcon.classList.toggle('hidden');
  });
  
  // Close mobile menu when clicking on a link
  const mobileLinks = document.querySelectorAll('.mobile-nav-link');
  mobileLinks.forEach(link => {
    link.addEventListener('click', function() {
      mobileMenu.classList.add('hidden');
      menuIcon.classList.remove('hidden');
      closeIcon.classList.add('hidden');
    });
  });
}

// Navbar scroll effect
function initNavbarScroll() {
  const navbar = document.getElementById('navbar');
  
  window.addEventListener('scroll', function() {
    if (window.scrollY > 20) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  });
}

// Smooth scrolling for anchor links
function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      e.preventDefault();
      
      const targetId = this.getAttribute('href').substring(1);
      if (!targetId) return;
      
      const targetElement = document.getElementById(targetId);
      if (!targetElement) return;
      
      window.scrollTo({
        top: targetElement.offsetTop - 100, // Offset for navbar
        behavior: 'smooth'
      });
    });
  });
}

// Animated logo
function initAnimatedLogo() {
  const canvas = document.getElementById('logo-canvas');
  if (!canvas) return;
  
  const ctx = canvas.getContext('2d');
  if (!ctx) return;
  
  const width = canvas.width;
  const height = canvas.height;
  
  let frame = 0;
  
  function drawLogo() {
    ctx.clearRect(0, 0, width, height);
    
    // Background circle
    ctx.beginPath();
    ctx.arc(width/2, height/2, 42 + Math.sin(frame/20) * 2, 0, Math.PI * 2);
    ctx.fillStyle = '#f3f3f3';
    ctx.fill();
    
    // GitHub-like octocat shape (simplified)
    ctx.beginPath();
    
    // Body
    const headSize = 28 + Math.sin(frame/15) * 1.5;
    ctx.arc(width/2, height/2 - 5, headSize, 0, Math.PI * 2);
    
    // Add tentacles
    for (let i = 0; i < 5; i++) {
      const angle = (i / 5) * Math.PI + frame / 40;
      const length = 22 + Math.sin(frame/10 + i) * 3;
      const startX = width/2 + Math.cos(angle) * headSize;
      const startY = height/2 - 5 + Math.sin(angle) * headSize;
      const endX = startX + Math.cos(angle) * length;
      const endY = startY + Math.sin(angle) * length;
      
      ctx.moveTo(startX, startY);
      ctx.quadraticCurveTo(
        startX + Math.cos(angle) * length * 0.6,
        startY + Math.sin(angle) * length * 0.6 + Math.sin(frame/10 + i * 2) * 5,
        endX,
        endY
      );
    }
    
    ctx.fillStyle = '#9b87f5';
    ctx.fill();
    
    // Create pulsating effect for stats visualization
    const barCount = 3;
    const barWidth = 4;
    const barSpacing = 8;
    const barStartX = width/2 - ((barCount * barWidth + (barCount-1) * barSpacing) / 2);
    
    for (let i = 0; i < barCount; i++) {
      const barHeight = 12 + Math.sin(frame/8 + i * 1.5) * 6;
      ctx.fillStyle = '#7E69AB';
      ctx.fillRect(
        barStartX + i * (barWidth + barSpacing),
        height/2 + 22,
        barWidth,
        barHeight
      );
    }
    
    frame++;
    requestAnimationFrame(drawLogo);
  }
  
  drawLogo();
}

// Intersection Observers for animations
function initIntersectionObservers() {
  // Dashboard preview observer
  const dashboardPreview = document.querySelector('.dashboard-preview');
  if (dashboardPreview) {
    const dashboardObserver = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting) {
          dashboardPreview.classList.add('visible');
        }
      },
      { threshold: 0.2 }
    );
    
    dashboardObserver.observe(dashboardPreview);
  }
}

// Initialize charts (using SVG for simplicity without recharts library)
function initCharts() {
  drawStarHistoryChart();
  drawWeeklyCommitChart();
}

function drawStarHistoryChart() {
  const container = document.getElementById('star-history-chart');
  if (!container) return;
  
  // Example data
  const starHistoryData = [
    { date: 'Jan', stars: 410 },
    { date: 'Feb', stars: 580 },
    { date: 'Mar', stars: 670 },
    { date: 'Apr', stars: 810 },
    { date: 'May', stars: 1020 },
    { date: 'Jun', stars: 1450 },
    { date: 'Jul', stars: 1890 },
    { date: 'Aug', stars: 2340 },
    { date: 'Sep', stars: 2780 },
    { date: 'Oct', stars: 3150 },
    { date: 'Nov', stars: 3580 },
    { date: 'Dec', stars: 4120 },
  ];
  
  // Create a simple SVG chart
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.setAttribute('width', '100%');
  svg.setAttribute('height', '100%');
  svg.style.overflow = 'visible';
  
  const margin = { top: 20, right: 20, bottom: 30, left: 40 };
  const width = 600 - margin.left - margin.right;
  const height = 300 - margin.top - margin.bottom;
  
  const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
  g.setAttribute('transform', `translate(${margin.left},${margin.top})`);
  
  // Create a grid
  for (let i = 0; i <= 5; i++) {
    const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    line.setAttribute('x1', 0);
    line.setAttribute('y1', i * height / 5);
    line.setAttribute('x2', width);
    line.setAttribute('y2', i * height / 5);
    line.setAttribute('stroke', '#f3f3f3');
    line.setAttribute('stroke-dasharray', '3,3');
    g.appendChild(line);
  }
  
  // Calculate scales
  const maxStars = Math.max(...starHistoryData.map(d => d.stars));
  
  // Create x-axis
  const xAxisGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
  xAxisGroup.setAttribute('transform', `translate(0,${height})`);
  
  starHistoryData.forEach((d, i) => {
    const x = i * (width / (starHistoryData.length - 1));
    
    // Tick
    const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    text.setAttribute('x', x);
    text.setAttribute('y', 20);
    text.setAttribute('text-anchor', 'middle');
    text.setAttribute('fill', '#666');
    text.setAttribute('font-size', '12px');
    text.textContent = d.date;
    xAxisGroup.appendChild(text);
  });
  
  // Create y-axis
  const yAxisGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
  
  for (let i = 0; i <= 5; i++) {
    const y = height - i * height / 5;
    const value = Math.round(i * maxStars / 5);
    
    // Tick text
    const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    text.setAttribute('x', -10);
    text.setAttribute('y', y);
    text.setAttribute('text-anchor', 'end');
    text.setAttribute('dominant-baseline', 'middle');
    text.setAttribute('fill', '#666');
    text.setAttribute('font-size', '12px');
    text.textContent = value;
    yAxisGroup.appendChild(text);
  }
  
  // Create the line path
  const linePath = document.createElementNS('http://www.w3.org/2000/svg', 'path');
  let pathData = 'M';
  
  starHistoryData.forEach((d, i) => {
    const x = i * (width / (starHistoryData.length - 1));
    const y = height - (d.stars / maxStars) * height;
    
    if (i === 0) {
      pathData += `${x},${y}`;
    } else {
      pathData += ` L${x},${y}`;
    }
    
    // Add dots
    const dot = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    dot.setAttribute('cx', x);
    dot.setAttribute('cy', y);
    dot.setAttribute('r', 4);
    dot.setAttribute('fill', '#9b87f5');
    g.appendChild(dot);
  });
  
  linePath.setAttribute('d', pathData);
  linePath.setAttribute('fill', 'none');
  linePath.setAttribute('stroke', '#9b87f5');
  linePath.setAttribute('stroke-width', '2.5');
  
  g.appendChild(linePath);
  g.appendChild(xAxisGroup);
  g.appendChild(yAxisGroup);
  svg.appendChild(g);
  
  container.appendChild(svg);
}

function drawWeeklyCommitChart() {
  const container = document.getElementById('weekly-commit-chart');
  if (!container) return;
  
  // Example data
  const commitData = [
    { name: 'Mon', value: 24 },
    { name: 'Tue', value: 13 },
    { name: 'Wed', value: 29 },
    { name: 'Thu', value: 32 },
    { name: 'Fri', value: 18 },
    { name: 'Sat', value: 8 },
    { name: 'Sun', value: 5 },
  ];
  
  // Create a simple SVG chart
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.setAttribute('width', '100%');
  svg.setAttribute('height', '100%');
  svg.style.overflow = 'visible';
  
  const margin = { top: 20, right: 20, bottom: 30, left: 40 };
  const width = 600 - margin.left - margin.right;
  const height = 300 - margin.top - margin.bottom;
  
  const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
  g.setAttribute('transform', `translate(${margin.left},${margin.top})`);
  
  // Create a grid (horizontal lines only)
  for (let i = 0; i <= 5; i++) {
    const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    line.setAttribute('x1', 0);
    line.setAttribute('y1', i * height / 5);
    line.setAttribute('x2', width);
    line.setAttribute('y2', i * height / 5);
    line.setAttribute('stroke', '#f3f3f3');
    line.setAttribute('stroke-dasharray', '3,3');
    g.appendChild(line);
  }
  
  // Calculate scales
  const maxValue = Math.max(...commitData.map(d => d.value));
  const barWidth = 28;
  const barPadding = (width / commitData.length - barWidth) / 2;
  
  // Create x-axis
  const xAxisGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
  xAxisGroup.setAttribute('transform', `translate(0,${height})`);
  
  // Create the base line
  const baseLine = document.createElementNS('http://www.w3.org/2000/svg', 'line');
  baseLine.setAttribute('x1', 0);
  baseLine.setAttribute('y1', 0);
  baseLine.setAttribute('x2', width);
  baseLine.setAttribute('y2', 0);
  baseLine.setAttribute('stroke', '#f3f3f3');
  xAxisGroup.appendChild(baseLine);
  
  commitData.forEach((d, i) => {
    const x = i * (width / commitData.length) + barPadding + barWidth / 2;
    
    // Tick text
    const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    text.setAttribute('x', x);
    text.setAttribute('y', 20);
    text.setAttribute('text-anchor', 'middle');
    text.setAttribute('fill', '#666');
    text.setAttribute('font-size', '12px');
    text.textContent = d.name;
    xAxisGroup.appendChild(text);
  });
  
  // Create y-axis
  const yAxisGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
  
  for (let i = 0; i <= 5; i++) {
    const y = height - i * height / 5;
    const value = Math.round(i * maxValue / 5);
    
    // Tick text
    const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    text.setAttribute('x', -10);
    text.setAttribute('y', y);
    text.setAttribute('text-anchor', 'end');
    text.setAttribute('dominant-baseline', 'middle');
    text.setAttribute('fill', '#666');
    text.setAttribute('font-size', '12px');
    text.textContent = value;
    yAxisGroup.appendChild(text);
  }
  
  // Create bars
  commitData.forEach((d, i) => {
    const x = i * (width / commitData.length) + barPadding;
    const barHeight = (d.value / maxValue) * height;
    const y = height - barHeight;
    
    const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    rect.setAttribute('x', x);
    rect.setAttribute('y', y);
    rect.setAttribute('width', barWidth);
    rect.setAttribute('height', barHeight);
    rect.setAttribute('fill', '#9b87f5');
    rect.setAttribute('rx', 4);
    rect.setAttribute('ry', 4);
    
    g.appendChild(rect);
  });
  
  g.appendChild(xAxisGroup);
  g.appendChild(yAxisGroup);
  svg.appendChild(g);
  
  container.appendChild(svg);
}
