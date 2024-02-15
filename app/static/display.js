function select_menu(id)
{
    menus = document.querySelectorAll('.menu .item a');
    for (let i = 0; i < menus.length; i++)
    {
        if (menus[i].id == id)
        {
            menus[i].className = "menu_item_actif";
        }
        else menus[i].className = "menu_item";
    }
}