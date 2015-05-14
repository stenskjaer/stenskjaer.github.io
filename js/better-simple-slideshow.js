var makeBSS = function (el, options) {
    // a collection of all of the slideshow
	var $slideshows = document.querySelectorAll(el), 
        $slideshow = {},
        Slideshow = {
            init: function (el, options) {
                this.counter = 0; // to keep track of current slide
                this.el = el; // current slideshow container    
                // a collection of all of the slides, caching for performance
				this.$items = el.querySelectorAll('figure'); 
                // total number of slides
				this.numItems = this.$items.length; 
                // if options object not passed in, then set to empty object
				options = options || {}; 
                // if options.auto object not passed in, then set to false
				options.auto = options.auto || false; 
                this.opts = {
                    auto: (typeof options.auto === "undefined") ?
						false : options.auto,
                    speed: (typeof options.auto.speed === "undefined") ?
						1500 : options.auto.speed,
                    pauseOnHover: (typeof
								   options.auto.pauseOnHover === "undefined") ?
						false : options.auto.pauseOnHover,
                    fullScreen: (typeof options.fullScreen === "undefined") ?
						false : options.fullScreen,
                    swipe: (typeof options.swipe === "undefined") ?
						true : options.swipe
                };
                
				// add show class to first figure 
                this.$items[0].classList.add('bss-show'); 
                this.injectControls(el);
				this.injectFinalFrame(el);
                this.addEventListeners(el);
                if (this.opts.auto) {
                    this.autoCycle(this.el, this.opts.speed,
								   this.opts.pauseOnHover);
                }
                if (this.opts.fullScreen) {
                    this.addFullScreen(this.el);
                }
                if (this.opts.swipe) {
                    this.addSwipe(this.el);
                }
            },
            showCurrent: function (i) {
                // increment or decrement this.counter depending on whether i
                // === 1 or i === -1
                if (i > 0) {
                    this.counter = (this.counter + 1 === this.numItems) ?
						-2 : this.counter + 1;
                } else {
                    this.counter = (this.counter - 1 < 0) ?
						this.numItems - 1 : this.counter - 1;
                }

                // remove .show from whichever element currently has it 
                // http://stackoverflow.com/a/16053538/2006057
                [].forEach.call(this.$items, function (el) {
                    el.classList.remove('bss-show');
                });
				
                // add .show to the one item that's supposed to have it
                if (this.counter == -2) {
					document.getElementById('final-frame').classList.add('bss-show');
				} else {
					this.$items[this.counter].classList.add('bss-show');					
				}
            },
			injectFinalFrame: function (el) {
				// Write the final frame of the show
				var finalFrame = document.createElement("figure");

				// Give it a class
				finalFrame.setAttribute('id', 'final-frame');

				// Give it some content
				finalFrame.innerHTML = '<div><h3>Stakken er tom!</h3> \
<p><a href="../../index.html">Hop tilbage til oversigten</a></p></div>';

				// Append to frame and then DOM
				el.appendChild(finalFrame);
			},
            injectControls: function (el) {
				// build and inject prev/next controls
                // first create all the new elements
                var spanPrev = document.createElement("span"),
                    spanNext = document.createElement("span"),
                    docFrag = document.createDocumentFragment();
				
                // add classes
                spanPrev.classList.add('bss-prev');
                spanNext.classList.add('bss-next');
				
                // add contents
                spanPrev.innerHTML = '&laquo;';
                spanNext.innerHTML = '&raquo;';
                
                // append elements to fragment, then append fragment to DOM
                docFrag.appendChild(spanPrev);
                docFrag.appendChild(spanNext);
                el.appendChild(docFrag);
            },
            addEventListeners: function (el) {
                var that = this;
                el.querySelector('.bss-next').addEventListener('click', function () {
                    that.showCurrent(1); // increment & show
                }, false);
				
                el.querySelector('.bss-prev').addEventListener('click', function () {
                    that.showCurrent(-1); // decrement & show
                }, false);
                
                el.onkeydown = function (e) {
                    e = e || window.event;
                    if (e.keyCode === 37) {
                        that.showCurrent(-1); // decrement & show
                    } else if (e.keyCode === 39) {
                        that.showCurrent(1); // increment & show
                    }
                };
            },
            autoCycle: function (el, speed, pauseOnHover) {
                var that = this,
                    interval = window.setInterval(function () {
                        that.showCurrent(1); // increment & show
                    }, speed);
                
                if (pauseOnHover) {
                    el.addEventListener('mouseover', function () {
                        interval = clearInterval(interval);
                    }, false);
                    el.addEventListener('mouseout', function () {
                        interval = window.setInterval(function () {
                            that.showCurrent(1); // increment & show
                        }, speed);
                    }, false);
                } // end pauseonhover
                
            },
            addFullScreen: function(el){
                var that = this,
					fsControl = document.createElement("span");
                
                fsControl.classList.add('bss-fullscreen');
                el.appendChild(fsControl);
                el.querySelector('.bss-fullscreen').addEventListener('click', function () {
                    that.toggleFullScreen(el);
                }, false);
            },
            addSwipe: function(el){
                var that = this,
                    ht = new Hammer(el);
                ht.on('swiperight', function(e) {
                    that.showCurrent(-1); // decrement & show
                });
                ht.on('swipeleft', function(e) {
                    that.showCurrent(1); // increment & show
                });
            },
            toggleFullScreen: function(el){
                // https://developer.mozilla.org/en-US/docs/Web/Guide/API/DOM/-
                // Using_full_screen_mode
				
				// alternative standard method
                if (!document.fullscreenElement && 
                    !document.mozFullScreenElement &&
					!document.webkitFullscreenElement &&   
                    !document.msFullscreenElement ) {  // current working methods
						if (document.documentElement.requestFullscreen) {
							el.requestFullscreen();
						} else if (document.documentElement.msRequestFullscreen) {
							el.msRequestFullscreen();
						} else if (document.documentElement.mozRequestFullScreen) {
							el.mozRequestFullScreen();
						} else if (document.documentElement.webkitRequestFullscreen) {
							el.webkitRequestFullscreen(el.ALLOW_KEYBOARD_INPUT);
						}
                } else {
                    if (document.exitFullscreen) {
						document.exitFullscreen();
                    } else if (document.msExitFullscreen) {
						document.msExitFullscreen();
                    } else if (document.mozCancelFullScreen) {
						document.mozCancelFullScreen();
                    } else if (document.webkitExitFullscreen) {
						document.webkitExitFullscreen();
                    }
                }
            } // end toggleFullScreen
            
        }; // end Slideshow object .....
    
    // make instances of Slideshow as needed
    [].forEach.call($slideshows, function (el) {
        $slideshow = Object.create(Slideshow);
        $slideshow.init(el, options);
    });
};
