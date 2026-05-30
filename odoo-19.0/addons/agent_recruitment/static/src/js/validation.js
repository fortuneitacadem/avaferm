/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.AgentRecruitment = publicWidget.Widget.extend({
    selector: '#agent_apply_form',
    events: {
        'change input[name="has_experience"]': '_onExperienceChange',
        'input #bio': '_onBioInput',
        'submit': '_onSubmit',
        'invalid': '_onInvalid',
        'input input, input select, input textarea': '_onInputClean',
    },

    start: function () {
        this._super.apply(this, arguments);
        this.$el.attr('novalidate', 'novalidate'); // Brauzer xabarlarini o'chirish
        console.log("Agent Recruitment JS Loaded with Custom Validation");
    },

    _onExperienceChange: function (ev) {
        const hasExperience = $(ev.currentTarget).val();
        const experienceDetailsDiv = $('#experience_details_div');
        const experienceDetailsTextarea = $('#experience_details');

        if (hasExperience === 'yes') {
            experienceDetailsDiv.removeClass('d-none');
            experienceDetailsTextarea.attr('required', 'required');
        } else {
            experienceDetailsDiv.addClass('d-none');
            experienceDetailsTextarea.removeAttr('required');
            this._removeError(experienceDetailsTextarea);
        }
    },

    _onBioInput: function (ev) {
        const bioText = $(ev.currentTarget).val();
        const count = bioText.length;
        const charCountSpan = $('#char_count');
        const counterDiv = $('#bio_counter');

        charCountSpan.text(count);

        if (count < 100) {
            counterDiv.removeClass('text-success').addClass('text-danger');
        } else {
            counterDiv.removeClass('text-danger').addClass('text-success');
            this._removeError($(ev.currentTarget));
        }
    },

    _onInvalid: function (ev) {
        ev.preventDefault();
        const input = $(ev.target);
        this._showError(input);
    },

    _onInputClean: function (ev) {
        const input = $(ev.currentTarget);
        if (input.val() || (input.attr('type') === 'checkbox' || input.attr('type') === 'radio')) {
            this._removeError(input);
        }
    },

    _onSubmit: function (ev) {
        const form = ev.currentTarget;
        if (!form.checkValidity()) {
            ev.preventDefault();
            const firstInvalid = $(form).find(':invalid').first();
            this._showError(firstInvalid);
            $('html, body').animate({
                scrollTop: firstInvalid.offset().top - 100
            }, 500);
        }
    },

    _showError: function (input) {
        this._removeError(input);
        input.addClass('is-invalid shake-animation');
        
        let message = "Iltimos, ushbu maydonni to'ldiring.";
        if (input.attr('id') === 'bio' && input.val().length < 100) {
            message = "Ma'lumot kamida 100 ta harf bo'lishi kerak.";
        } else if (input.attr('type') === 'email' && input.val()) {
            message = "Iltimos, to'g'ri email kiriting.";
        } else if (input.attr('type') === 'tel' && input.val()) {
            message = "Iltimos, to'g'ri telefon raqam kiriting.";
        }

        const errorTag = $('<div class="error-message">' + message + '</div>');
        input.after(errorTag);
        errorTag.fadeIn();

        setTimeout(() => {
            input.removeClass('shake-animation');
        }, 500);
    },

    _removeError: function (input) {
        input.removeClass('is-invalid');
        input.parent().find('.error-message').remove();
    },
});

export default publicWidget.registry.AgentRecruitment;
