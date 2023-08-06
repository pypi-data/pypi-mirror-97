import MainWindow from "./MainWindow/MainWindow";
export function activate(context) {
    context.registerPlugin({
        type: 'MainWindow',
        name: 'MainWindow',
        label: 'Main Window',
        component: MainWindow
    });
}
//# sourceMappingURL=mainwindow.js.map