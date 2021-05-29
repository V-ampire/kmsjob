"use strict";


class App {
    constructor() {
        this.selectors = {
            search: {
                togglerClass: 'search-toggler',
                containerClass: 'search-container',
                activeClass: 'search-active'
            },
            register: {
                togglerClass: 'register-toggler',
                containerClass: 'register-container',
                activeClass: 'register-active',
            },
            login: {
                togglerClass: 'login-toggler',
                containerClass: 'login-container',
                activeClass: 'login-active',
            },
            logout: {
                togglerClass: 'logout-toggler',
                containerClass: 'logout-container',
                activeClass: 'logout-active',
            },
            currentDateFormId: 'currentDateForm',
            currentDateInput: 'current_date',
            currentDateTextClass: 'current-date-text',
            datetimepickerWidgetClass: 'bootstrap-datetimepicker-widget',
            paginationClass: 'pagination',
            msgModalClass: 'messages-modal',
        };
        this.styles = {
            searchActiveStyle: 'left: 0',
            searchUnActiveStyle: 'left: -120%',
            registerActiveStyle: 'top: 0',
            registerUnActiveStyle: 'top: -120%',
        };
        const msgContainer = document.querySelector('.'+this.selectors.msgModalClass)
            .querySelector('.modal-body');
        this.msgCtrl = new MessageCtrl(msgContainer);
        this.currentScreenMode;
    }

    init() {
        document.body.clientWidth >= 768 ? this.currentScreenMode = 'desctop' : 'mobile';
        this.setDateTimePickers();
        this.loadEventListeners();
        this.adaptLayout();
        this.initMsgCtrl();
    }

    setDateTimePickers() {
        const options = {
            locale: 'ru',
            format: 'L',
            icons: {
                date: 'calendar-alt',
            },
        };
            $('#datetimepicker-from').datetimepicker(options);
            $('#datetimepicker-to').datetimepicker(options);
            if ($('#datetimepicker-calendar')) {
                $('#datetimepicker-calendar').datetimepicker(options);
            };
    };

    toggleBar(bar) {
        /* 
            Show toolbar
            Accept object of toolbar selectors consist of 
            {
                containerClass: ...,
                togglerClass: ...,
                activeClass: ....
            }
        */
       console.log(bar);
        const toolbar = document.querySelector('.'+bar.containerClass);
        toolbar.classList.toggle(bar.activeClass)
        
    };

    adaptLayout() {
        // Resize pagination
        const pagination = document.querySelector('.'+this.selectors.paginationClass);
        if (document.body.clientWidth >= 768 && pagination) {
            pagination.classList.remove('pagination-sm');
        }
        // Checkout ads format
        if (document.body.clientWidth === 768) {
            console.log('checkout');
        }
    }

    loadEventListeners() {
        // Add event listeners to show search-bar
        document.querySelectorAll('.'+this.selectors.search.togglerClass).forEach((toggler) => {
            toggler.addEventListener('click', () => {this.toggleBar(this.selectors.search)});
        });
        // Add event listeners to show register-bar
        document.querySelectorAll('.'+this.selectors.register.togglerClass).forEach((toggler) => {
            toggler.addEventListener('click', () => {this.toggleBar(this.selectors.register)});
        });
        // Add event listeners to show login-bar
        document.querySelectorAll('.'+this.selectors.login.togglerClass).forEach((toggler) => {
            toggler.addEventListener('click', () => {this.toggleBar(this.selectors.login)});
        });
        // Add event listeners to show logout-bar
        document.querySelectorAll('.'+this.selectors.logout.togglerClass).forEach((toggler) => {
            toggler.addEventListener('click', () => {this.toggleBar(this.selectors.logout)});
        });
        // Add listener on change current date
        // const currentDate = document.querySelector('.'+this.selectors.currentDateTextClass);
        $('#datetimepicker-calendar').on('change.datetimepicker', (e) => {
            //console.log('ok');
            // Send current date form
            if (e.oldDate && e.oldDate.format('DD.MM.YYYY') !== e.date.format('DD.MM.YYYY')) {
                const form = document.getElementById(this.selectors.currentDateFormId);
                form.submit();
            }
        });
        // Hide datetimepicker-calendar widget when clicking on out of widget
        document.addEventListener('click', (e) => {
            if (!e.target.closest('#datetimepicker-calendar')) {
                if ($('.'+this.selectors.datetimepickerWidgetClass).is(':visible')) {
                    $('#datetimepicker-calendar').datetimepicker('hide');
                };
            };
        });
        // Adapt layout changing screen size
        $( window ).resize(() => {
            this.adaptLayout();
        });
    };

    initMsgCtrl() {
        if (messages.length) {
            this.msgCtrl.renderMessages(messages);
            $('.'+this.selectors.msgModalClass).modal('show');
        };
    };
}

const app = new App();
app.init();