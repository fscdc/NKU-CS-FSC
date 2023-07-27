// 在页面加载完毕后执行以下代码
document.addEventListener('DOMContentLoaded', function() {
    // 获取下拉菜单的按钮和菜单元素
    const dropdownButton = document.querySelector('.dropdown-button');
    const dropdownMenu = document.querySelector('.dropdown-menu');

    // 点击按钮时切换菜单的显示状态
    dropdownButton.addEventListener('click', function() {
        dropdownMenu.classList.toggle('show');
    });

    // 点击菜单以外的区域时隐藏菜单
    document.addEventListener('click', function(event) {
        if (!dropdownButton.contains(event.target) && !dropdownMenu.contains(event.target)) {
            dropdownMenu.classList.remove('show');
        }
    });
});