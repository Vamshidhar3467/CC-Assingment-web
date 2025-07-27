// TALYOUTH SDG Leadership Platform - Main JavaScript File

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initializeApp();
});

// Main initialization function
function initializeApp() {
    // Initialize Bootstrap components
    initializeBootstrap();
    
    // Initialize form handling
    initializeForms();
    
    // Initialize navigation
    initializeNavigation();
    
    // Initialize video components
    initializeVideoComponents();
    
    // Initialize progress tracking
    initializeProgressTracking();
    
    // Initialize rating systems
    initializeRatingSystems();
    
    // Initialize animations
    initializeAnimations();
    
    // Initialize tooltips and popovers
    initializeTooltips();
    
    // Initialize search functionality
    initializeSearch();
    
    // Initialize feedback forms
    initializeFeedbackForms();
    
    // Initialize character counters
    initializeCharacterCounters();
    
    console.log('TALYOUTH Platform initialized successfully');
}

// Bootstrap Components Initialization
function initializeBootstrap() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Initialize modals
    var modalTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="modal"]'));
    modalTriggerList.forEach(function(modalTrigger) {
        modalTrigger.addEventListener('click', function() {
            var targetModal = document.querySelector(modalTrigger.getAttribute('data-bs-target'));
            if (targetModal) {
                var modal = new bootstrap.Modal(targetModal);
                modal.show();
            }
        });
    });
    
    // Auto-dismiss alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert-dismissible');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
}

// Form Handling
function initializeForms() {
    // Add form validation
    var forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
    
    // Handle form submissions with loading states
    var submitButtons = document.querySelectorAll('form button[type="submit"]');
    submitButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            var form = button.closest('form');
            if (form && form.checkValidity()) {
                showLoadingState(button);
            }
        });
    });
    
    // Auto-save form data to localStorage
    var autoSaveForms = document.querySelectorAll('.auto-save');
    autoSaveForms.forEach(function(form) {
        var formId = form.id || 'unnamed-form';
        
        // Load saved data
        loadFormData(form, formId);
        
        // Save data on input
        form.addEventListener('input', function() {
            saveFormData(form, formId);
        });
    });
}

// Navigation Enhancement
function initializeNavigation() {
    // Mobile menu toggle
    var navbarToggler = document.querySelector('.navbar-toggler');
    if (navbarToggler) {
        navbarToggler.addEventListener('click', function() {
            var navbar = document.querySelector('.navbar-collapse');
            navbar.classList.toggle('show');
        });
    }
    
    // Smooth scrolling for anchor links
    var anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            var targetId = link.getAttribute('href');
            var targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                e.preventDefault();
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Active navigation highlighting
    highlightActiveNavigation();
    
    // Breadcrumb navigation
    updateBreadcrumbs();
}

// Video Components
function initializeVideoComponents() {
    // Video progress tracking
    var videos = document.querySelectorAll('video');
    videos.forEach(function(video) {
        video.addEventListener('loadedmetadata', function() {
            updateVideoMetadata(video);
        });
        
        video.addEventListener('timeupdate', function() {
            updateVideoProgress(video);
        });
        
        video.addEventListener('ended', function() {
            markVideoComplete(video);
        });
    });
    
    // Video playlist functionality
    initializeVideoPlaylist();
    
    // Video speed controls
    addVideoSpeedControls();
    
    // Video bookmark functionality
    initializeVideoBookmarks();
}

// Progress Tracking
function initializeProgressTracking() {
    // Animate progress bars
    var progressBars = document.querySelectorAll('.progress-bar');
    progressBars.forEach(function(bar) {
        var targetWidth = bar.style.width || bar.getAttribute('data-width') || '0%';
        bar.style.width = '0%';
        
        setTimeout(function() {
            bar.style.width = targetWidth;
        }, 500);
    });
    
    // Update progress statistics
    updateProgressStats();
    
    // Save progress to server
    saveProgressToServer();
}

// Rating Systems
function initializeRatingSystems() {
    var ratingContainers = document.querySelectorAll('.rating-stars');
    
    ratingContainers.forEach(function(container) {
        var stars = container.querySelectorAll('.star');
        var ratingInput = container.parentElement.querySelector('input[type="hidden"]');
        var ratingName = container.getAttribute('data-rating');
        
        stars.forEach(function(star, index) {
            star.addEventListener('click', function() {
                var rating = index + 1;
                updateStarRating(container, rating);
                
                if (ratingInput) {
                    ratingInput.value = rating;
                }
                
                // Trigger custom event
                var event = new CustomEvent('ratingChanged', {
                    detail: { rating: rating, name: ratingName }
                });
                container.dispatchEvent(event);
            });
            
            star.addEventListener('mouseenter', function() {
                highlightStars(container, index + 1);
            });
        });
        
        container.addEventListener('mouseleave', function() {
            var currentRating = ratingInput ? parseInt(ratingInput.value) : 0;
            updateStarRating(container, currentRating);
        });
    });
}

// Animation Initialization
function initializeAnimations() {
    // Intersection Observer for scroll animations
    var animatedElements = document.querySelectorAll('.animate-on-scroll');
    
    if (animatedElements.length > 0) {
        var observer = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animated');
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });
        
        animatedElements.forEach(function(element) {
            observer.observe(element);
        });
    }
    
    // Counter animations
    animateCounters();
    
    // Typewriter effect
    initializeTypewriterEffect();
}

// Tooltip and Popover Initialization
function initializeTooltips() {
    // Dynamic tooltip content
    var dynamicTooltips = document.querySelectorAll('[data-dynamic-tooltip]');
    dynamicTooltips.forEach(function(element) {
        element.addEventListener('mouseenter', function() {
            updateDynamicTooltip(element);
        });
    });
    
    // Progress tooltips
    var progressElements = document.querySelectorAll('.progress-bar');
    progressElements.forEach(function(element) {
        var tooltip = new bootstrap.Tooltip(element, {
            title: function() {
                return 'Progress: ' + element.style.width;
            }
        });
    });
}

// Search Functionality
function initializeSearch() {
    var searchInputs = document.querySelectorAll('.search-input');
    
    searchInputs.forEach(function(input) {
        var searchContainer = input.closest('.search-container');
        var searchResults = searchContainer.querySelector('.search-results');
        
        input.addEventListener('input', function() {
            var query = input.value.trim();
            
            if (query.length >= 2) {
                performSearch(query, searchResults);
            } else {
                clearSearchResults(searchResults);
            }
        });
        
        // Handle search result clicks
        if (searchResults) {
            searchResults.addEventListener('click', function(e) {
                var resultItem = e.target.closest('.search-result-item');
                if (resultItem) {
                    handleSearchResultClick(resultItem, input);
                }
            });
        }
    });
    
    // Course filtering
    initializeCourseFiltering();
    
    // Video library search
    initializeVideoSearch();
}

// Feedback Forms
function initializeFeedbackForms() {
    var feedbackForms = document.querySelectorAll('.feedback-form');
    
    feedbackForms.forEach(function(form) {
        // Auto-expand textareas
        var textareas = form.querySelectorAll('textarea');
        textareas.forEach(function(textarea) {
            textarea.addEventListener('input', function() {
                autoExpandTextarea(textarea);
            });
        });
        
        // Form validation
        form.addEventListener('submit', function(e) {
            if (!validateFeedbackForm(form)) {
                e.preventDefault();
                showFormErrors(form);
            }
        });
        
        // Save draft functionality
        var saveDraftBtn = form.querySelector('.save-draft');
        if (saveDraftBtn) {
            saveDraftBtn.addEventListener('click', function() {
                saveFeedbackDraft(form);
            });
        }
    });
}

// Character Counters
function initializeCharacterCounters() {
    var textareasWithCounter = document.querySelectorAll('textarea[maxlength]');
    
    textareasWithCounter.forEach(function(textarea) {
        var maxLength = parseInt(textarea.getAttribute('maxlength'));
        var counterId = textarea.id + 'Counter';
        var counter = document.getElementById(counterId);
        
        if (counter) {
            textarea.addEventListener('input', function() {
                var currentLength = textarea.value.length;
                counter.textContent = currentLength;
                
                // Update counter color based on usage
                var usagePercentage = (currentLength / maxLength) * 100;
                
                if (usagePercentage >= 90) {
                    counter.style.color = '#dc3545'; // Danger
                } else if (usagePercentage >= 75) {
                    counter.style.color = '#ffc107'; // Warning
                } else {
                    counter.style.color = '#6c757d'; // Default
                }
            });
            
            // Initialize counter
            textarea.dispatchEvent(new Event('input'));
        }
    });
}

// Utility Functions

function showLoadingState(button) {
    button.disabled = true;
    var originalText = button.innerHTML;
    button.setAttribute('data-original-text', originalText);
    button.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
    
    // Reset after 30 seconds if no response
    setTimeout(function() {
        if (button.disabled) {
            hideLoadingState(button);
        }
    }, 30000);
}

function hideLoadingState(button) {
    button.disabled = false;
    var originalText = button.getAttribute('data-original-text');
    if (originalText) {
        button.innerHTML = originalText;
        button.removeAttribute('data-original-text');
    }
}

function saveFormData(form, formId) {
    var formData = new FormData(form);
    var dataObj = {};
    
    for (var pair of formData.entries()) {
        dataObj[pair[0]] = pair[1];
    }
    
    localStorage.setItem('talyouth_' + formId, JSON.stringify(dataObj));
}

function loadFormData(form, formId) {
    var savedData = localStorage.getItem('talyouth_' + formId);
    
    if (savedData) {
        try {
            var dataObj = JSON.parse(savedData);
            
            for (var key in dataObj) {
                var input = form.querySelector('[name="' + key + '"]');
                if (input) {
                    input.value = dataObj[key];
                }
            }
        } catch (e) {
            console.warn('Error loading saved form data:', e);
        }
    }
}

function updateStarRating(container, rating) {
    var stars = container.querySelectorAll('.star');
    
    stars.forEach(function(star, index) {
        if (index < rating) {
            star.classList.add('active');
        } else {
            star.classList.remove('active');
        }
    });
}

function highlightStars(container, rating) {
    var stars = container.querySelectorAll('.star');
    
    stars.forEach(function(star, index) {
        if (index < rating) {
            star.style.color = '#FFD700';
        } else {
            star.style.color = '#E9ECEF';
        }
    });
}

function updateVideoProgress(video) {
    var progress = (video.currentTime / video.duration) * 100;
    var videoId = video.getAttribute('data-video-id');
    
    if (videoId) {
        // Send progress to server
        fetch('/api/video-progress', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                video_id: videoId,
                progress: progress,
                current_time: video.currentTime
            })
        }).catch(function(error) {
            console.warn('Error saving video progress:', error);
        });
    }
}

function markVideoComplete(video) {
    var videoId = video.getAttribute('data-video-id');
    
    if (videoId) {
        fetch('/api/video-complete', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                video_id: videoId
            })
        }).then(function(response) {
            if (response.ok) {
                showNotification('Video completed successfully!', 'success');
                updateProgressStats();
            }
        }).catch(function(error) {
            console.warn('Error marking video complete:', error);
        });
    }
}

function performSearch(query, resultsContainer) {
    // Show loading state
    resultsContainer.innerHTML = '<div class="search-loading">Searching...</div>';
    
    fetch('/api/search?q=' + encodeURIComponent(query))
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            displaySearchResults(data, resultsContainer);
        })
        .catch(function(error) {
            console.warn('Search error:', error);
            resultsContainer.innerHTML = '<div class="search-error">Search failed. Please try again.</div>';
        });
}

function displaySearchResults(results, container) {
    if (results.length === 0) {
        container.innerHTML = '<div class="search-no-results">No results found.</div>';
        return;
    }
    
    var html = '<div class="search-results-list">';
    results.forEach(function(result) {
        html += '<div class="search-result-item" data-url="' + result.url + '">';
        html += '<div class="result-title">' + result.title + '</div>';
        html += '<div class="result-description">' + result.description + '</div>';
        html += '</div>';
    });
    html += '</div>';
    
    container.innerHTML = html;
}

function clearSearchResults(container) {
    if (container) {
        container.innerHTML = '';
    }
}

function handleSearchResultClick(resultItem, searchInput) {
    var url = resultItem.getAttribute('data-url');
    var title = resultItem.querySelector('.result-title').textContent;
    
    // Update search input
    searchInput.value = title;
    
    // Navigate to result
    if (url) {
        window.location.href = url;
    }
}

function autoExpandTextarea(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
}

function validateFeedbackForm(form) {
    var isValid = true;
    var requiredFields = form.querySelectorAll('[required]');
    
    requiredFields.forEach(function(field) {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });
    
    // Validate ratings
    var ratingGroups = form.querySelectorAll('.rating-stars');
    ratingGroups.forEach(function(group) {
        var hiddenInput = group.parentElement.querySelector('input[type="hidden"]');
        if (hiddenInput && hiddenInput.hasAttribute('required') && !hiddenInput.value) {
            group.classList.add('is-invalid');
            isValid = false;
        } else {
            group.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

function showFormErrors(form) {
    var firstError = form.querySelector('.is-invalid');
    if (firstError) {
        firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
        firstError.focus();
    }
}

function saveFeedbackDraft(form) {
    var formData = new FormData(form);
    var draftData = {};
    
    for (var pair of formData.entries()) {
        draftData[pair[0]] = pair[1];
    }
    
    fetch('/api/save-feedback-draft', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(draftData)
    }).then(function(response) {
        if (response.ok) {
            showNotification('Draft saved successfully!', 'success');
        } else {
            showNotification('Error saving draft.', 'error');
        }
    }).catch(function(error) {
        console.warn('Error saving draft:', error);
        showNotification('Error saving draft.', 'error');
    });
}

function showNotification(message, type) {
    var notification = document.createElement('div');
    notification.className = 'alert alert-' + type + ' alert-dismissible fade show position-fixed';
    notification.style.top = '20px';
    notification.style.right = '20px';
    notification.style.zIndex = '9999';
    notification.style.minWidth = '300px';
    
    notification.innerHTML = message + 
        '<button type="button" class="btn-close" data-bs-dismiss="alert"></button>';
    
    document.body.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(function() {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 5000);
}

function highlightActiveNavigation() {
    var currentPath = window.location.pathname;
    var navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    navLinks.forEach(function(link) {
        var linkPath = new URL(link.href).pathname;
        if (linkPath === currentPath) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
}

function updateBreadcrumbs() {
    var breadcrumbContainer = document.querySelector('.breadcrumb');
    if (!breadcrumbContainer) return;
    
    var pathSegments = window.location.pathname.split('/').filter(function(segment) {
        return segment.length > 0;
    });
    
    var breadcrumbHTML = '<li class="breadcrumb-item"><a href="/">Home</a></li>';
    var currentPath = '';
    
    pathSegments.forEach(function(segment, index) {
        currentPath += '/' + segment;
        var isLast = index === pathSegments.length - 1;
        var segmentName = segment.charAt(0).toUpperCase() + segment.slice(1).replace(/[-_]/g, ' ');
        
        if (isLast) {
            breadcrumbHTML += '<li class="breadcrumb-item active">' + segmentName + '</li>';
        } else {
            breadcrumbHTML += '<li class="breadcrumb-item"><a href="' + currentPath + '">' + segmentName + '</a></li>';
        }
    });
    
    breadcrumbContainer.innerHTML = breadcrumbHTML;
}

function animateCounters() {
    var counters = document.querySelectorAll('.counter');
    
    counters.forEach(function(counter) {
        var target = parseInt(counter.getAttribute('data-target')) || 0;
        var duration = parseInt(counter.getAttribute('data-duration')) || 2000;
        var start = 0;
        var increment = target / (duration / 16);
        
        var timer = setInterval(function() {
            start += increment;
            counter.textContent = Math.floor(start);
            
            if (start >= target) {
                counter.textContent = target;
                clearInterval(timer);
            }
        }, 16);
    });
}

function initializeTypewriterEffect() {
    var typewriterElements = document.querySelectorAll('.typewriter');
    
    typewriterElements.forEach(function(element) {
        var text = element.getAttribute('data-text') || element.textContent;
        var speed = parseInt(element.getAttribute('data-speed')) || 100;
        
        element.textContent = '';
        
        var i = 0;
        var timer = setInterval(function() {
            if (i < text.length) {
                element.textContent += text.charAt(i);
                i++;
            } else {
                clearInterval(timer);
            }
        }, speed);
    });
}

function updateProgressStats() {
    // This would typically fetch updated stats from the server
    var progressElements = document.querySelectorAll('[data-progress-update]');
    
    progressElements.forEach(function(element) {
        // Simulate progress update
        var currentProgress = parseInt(element.textContent) || 0;
        if (currentProgress < 100) {
            element.textContent = Math.min(currentProgress + 1, 100) + '%';
        }
    });
}

function saveProgressToServer() {
    var progressData = {
        current_page: window.location.pathname,
        timestamp: new Date().toISOString(),
        user_agent: navigator.userAgent
    };
    
    fetch('/api/track-progress', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(progressData)
    }).catch(function(error) {
        console.warn('Error tracking progress:', error);
    });
}

function initializeVideoPlaylist() {
    var playlistItems = document.querySelectorAll('.playlist-item');
    
    playlistItems.forEach(function(item, index) {
        item.addEventListener('click', function() {
            playVideoFromPlaylist(index);
            updatePlaylistUI(index);
        });
    });
}

function playVideoFromPlaylist(index) {
    var videos = document.querySelectorAll('.playlist-video');
    var currentVideo = videos[index];
    
    if (currentVideo) {
        // Hide all videos
        videos.forEach(function(video) {
            video.style.display = 'none';
            video.pause();
        });
        
        // Show and play selected video
        currentVideo.style.display = 'block';
        currentVideo.play();
    }
}

function updatePlaylistUI(activeIndex) {
    var playlistItems = document.querySelectorAll('.playlist-item');
    
    playlistItems.forEach(function(item, index) {
        if (index === activeIndex) {
            item.classList.add('active');
        } else {
            item.classList.remove('active');
        }
    });
}

function addVideoSpeedControls() {
    var videos = document.querySelectorAll('video');
    
    videos.forEach(function(video) {
        var speedControls = document.createElement('div');
        speedControls.className = 'video-speed-controls';
        speedControls.innerHTML = `
            <button onclick="changeVideoSpeed(this, 0.5)">0.5x</button>
            <button onclick="changeVideoSpeed(this, 1)" class="active">1x</button>
            <button onclick="changeVideoSpeed(this, 1.25)">1.25x</button>
            <button onclick="changeVideoSpeed(this, 1.5)">1.5x</button>
            <button onclick="changeVideoSpeed(this, 2)">2x</button>
        `;
        
        video.parentNode.appendChild(speedControls);
    });
}

function changeVideoSpeed(button, speed) {
    var video = button.parentNode.previousElementSibling;
    if (video && video.tagName === 'VIDEO') {
        video.playbackRate = speed;
        
        // Update active button
        var buttons = button.parentNode.querySelectorAll('button');
        buttons.forEach(function(btn) {
            btn.classList.remove('active');
        });
        button.classList.add('active');
    }
}

function initializeVideoBookmarks() {
    var videos = document.querySelectorAll('video[data-video-id]');
    
    videos.forEach(function(video) {
        video.addEventListener('dblclick', function() {
            addVideoBookmark(video, video.currentTime);
        });
    });
}

function addVideoBookmark(video, time) {
    var videoId = video.getAttribute('data-video-id');
    var bookmarkData = {
        video_id: videoId,
        time: time,
        note: prompt('Add a note for this bookmark (optional):') || ''
    };
    
    fetch('/api/video-bookmark', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(bookmarkData)
    }).then(function(response) {
        if (response.ok) {
            showNotification('Bookmark added successfully!', 'success');
        }
    }).catch(function(error) {
        console.warn('Error adding bookmark:', error);
    });
}

function initializeCourseFiltering() {
    var filterButtons = document.querySelectorAll('.course-filter');
    var courseCards = document.querySelectorAll('.course-card');
    
    filterButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            var filterValue = button.getAttribute('data-filter');
            
            // Update active filter button
            filterButtons.forEach(function(btn) {
                btn.classList.remove('active');
            });
            button.classList.add('active');
            
            // Filter courses
            courseCards.forEach(function(card) {
                var cardSDG = card.getAttribute('data-sdg');
                
                if (filterValue === 'all' || cardSDG === filterValue) {
                    card.style.display = 'block';
                    card.classList.add('fade-in');
                } else {
                    card.style.display = 'none';
                    card.classList.remove('fade-in');
                }
            });
        });
    });
}

function initializeVideoSearch() {
    var videoSearchInput = document.querySelector('#videoSearch');
    var videoCards = document.querySelectorAll('.video-card');
    
    if (videoSearchInput) {
        videoSearchInput.addEventListener('input', function() {
            var query = videoSearchInput.value.toLowerCase().trim();
            
            videoCards.forEach(function(card) {
                var title = card.querySelector('.video-title').textContent.toLowerCase();
                var description = card.querySelector('.video-description').textContent.toLowerCase();
                
                if (title.includes(query) || description.includes(query)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }
}

// Global error handling
window.addEventListener('error', function(event) {
    console.error('JavaScript error:', event.error);
    
    // Send error to server for logging
    fetch('/api/log-error', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            message: event.message,
            filename: event.filename,
            lineno: event.lineno,
            colno: event.colno,
            error: event.error ? event.error.stack : null,
            url: window.location.href,
            userAgent: navigator.userAgent
        })
    }).catch(function(error) {
        console.warn('Error logging failed:', error);
    });
});

// Service Worker registration for offline functionality
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/sw.js')
            .then(function(registration) {
                console.log('ServiceWorker registration successful');
            })
            .catch(function(error) {
                console.log('ServiceWorker registration failed');
            });
    });
}

// Export functions for global access
window.TALYOUTH = {
    showNotification: showNotification,
    updateStarRating: updateStarRating,
    changeVideoSpeed: changeVideoSpeed,
    showLoadingState: showLoadingState,
    hideLoadingState: hideLoadingState
};