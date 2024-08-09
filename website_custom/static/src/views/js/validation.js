/* @odoo-module */  
import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.s_website_form_my = publicWidget.Widget.extend({
    selector: '.s_website_form_my',
    
    start: function () {
        this._super.apply(this,arguments);
        this._bindEvents();
        this.passwordInput = document.querySelector(".password_input");
        this.emailInput = document.querySelector(".email_input");
        this.errorMessage = document.querySelector("#s_website_form_result_my");
    },

    _bindEvents: function () {
        this.$('.s_website_form_send_my').on('click', this._send.bind(this));
    },

    _send: function () {
        var password = this.passwordInput.value;
        var email = this.emailInput.value;

        const passwordError = this._validatePassword(password);
        const emailError = this._validateEmail(email)
        if (emailError === "success" && passwordError === "success"){
            this.$el.find('form').submit();
        }else{
            this.errorMessage.textContent = emailError !== "success" ? emailError : passwordError;
        }
    },
    _validateEmail: function (email) {
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (!emailPattern.test(email)) {
            return 'Please enter a valid email address.';
        }
        return 'success';
    },
    _validatePassword: function (password) {
        const minLength = 8;
        const capitalLetter = /[A-Z]/;
        const smallLetter = /[a-z]/;
        const number = /[0-9]/;
        const specialCharacter = /[!@#$%^&*(),.?":{}|<>]/;

        if (password.length < minLength) {
            return 'Password must be at least 8 characters long.';
        }
        if (!capitalLetter.test(password)) {
            return 'Password must contain at least one uppercase letter.';
        }
        if (!smallLetter.test(password)) {
            return 'Password must contain at least one lowercase letter.';
        }
        if (!number.test(password)) {
            return 'Password must contain at least one number.';
        }
        if (!specialCharacter.test(password)) {
            return 'Password must contain at least one special character.';
        }
        return 'success';
    },

});

export default publicWidget.registry.s_website_form_my;