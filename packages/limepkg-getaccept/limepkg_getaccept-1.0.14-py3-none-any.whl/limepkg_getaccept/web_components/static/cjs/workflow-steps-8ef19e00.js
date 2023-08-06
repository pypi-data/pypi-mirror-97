'use strict';

const EnumViews = require('./EnumViews-bbc19da7.js');

const workflowSteps = [
    {
        currentView: EnumViews.EnumViews.recipient,
        previousView: EnumViews.EnumViews.home,
        nextView: EnumViews.EnumViews.selectFile,
        label: 'Select recipient',
    },
    {
        currentView: EnumViews.EnumViews.selectFile,
        previousView: EnumViews.EnumViews.recipient,
        nextView: EnumViews.EnumViews.sendDocument,
        label: 'Select document',
    },
    {
        currentView: EnumViews.EnumViews.sendDocument,
        previousView: EnumViews.EnumViews.selectFile,
        nextView: EnumViews.EnumViews.documentValidation,
        label: 'Prepare sendout',
    },
    {
        currentView: EnumViews.EnumViews.documentValidation,
        previousView: EnumViews.EnumViews.sendDocument,
        nextView: EnumViews.EnumViews.documentValidation,
        label: 'Send document',
    },
];

exports.workflowSteps = workflowSteps;
