import { E as EnumViews } from './EnumViews-26a35d6d.js';

const workflowSteps = [
    {
        currentView: EnumViews.recipient,
        previousView: EnumViews.home,
        nextView: EnumViews.selectFile,
        label: 'Select recipient',
    },
    {
        currentView: EnumViews.selectFile,
        previousView: EnumViews.recipient,
        nextView: EnumViews.sendDocument,
        label: 'Select document',
    },
    {
        currentView: EnumViews.sendDocument,
        previousView: EnumViews.selectFile,
        nextView: EnumViews.documentValidation,
        label: 'Prepare sendout',
    },
    {
        currentView: EnumViews.documentValidation,
        previousView: EnumViews.sendDocument,
        nextView: EnumViews.documentValidation,
        label: 'Send document',
    },
];

export { workflowSteps as w };
