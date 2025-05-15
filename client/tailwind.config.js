/** @type {import('tailwindcss').Config} */

module.exports = {
    content: [
        './src/**/*.{js,ts,jsx,tsx,mdx}',
    ],
    theme: {
        extend: {
            backgroundColor: {
                primary: '#F6F1F1',
                secondary: '#e5e7eb',
            },
            textColor: {
                primary: '#000000',
            },
            borderColor: {
                primary: '#CFCFCF',
            },

        },
    },
    plugins: [],
};
