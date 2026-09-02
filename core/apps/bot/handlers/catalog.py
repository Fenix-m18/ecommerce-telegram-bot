from aiogram import types
from aiogram.dispatcher.filters import Text
from asgiref.sync import sync_to_async

from core.apps.bot.handlers.authorization import sign_in
from core.apps.bot.keyboards import sign_inup_kb
from core.apps.bot.keyboards.catalog_ikb import get_categories, get_subcategories, category_cb, subcategory_cb
from core.apps.bot.keyboards.default_kb import markup
from core.apps.bot.loader import bot, dp
from core.apps.bot.models import Product, SubCategory, Category


async def show_categories(message: types.Message):
    if sign_in['current_state']:
        if await category_exists():
            await bot.send_message(
                chat_id=message.chat.id, text="Please choose a category from the list 📂",
                reply_markup=await get_categories(),
            )
        else:
            await bot.send_message(
                chat_id=message.chat.id, text="Unfortunately, the administrator hasn't added any categories yet ☹️",
                reply_markup=markup,
            )
    else:
        await message.answer(
            "You are not logged in, please try logging into your profile ‼️",
            reply_markup=sign_inup_kb.markup,
        )


async def get_products(query):
    elem = query.data.split(':')
    if await subcategory_products_exists(product_subcategory_id=elem[1]):
        await bot.send_message(
            chat_id=query.message.chat.id,
            text="Here is the list of products available in this subcategor 👇",
        )
        products = await get_subcategory_products_list(elem[1])

for product in products:
    # 1. Захист від занадто довгого опису (ліміт Telegram 1024 символи)
    description = product.description or ""
    if len(description) > 900:
        description = description[:897] + "..."

    text = f"🚀: {product.name}\n\n" \
           f"💬: {description}\n\n" \
           f"Ціна 💰: {product.price} грн"

    # 2. Передаємо URL-адресу Cloudinary замість зчитування локального файлу
    if product.photo:
        await bot.send_photo(
            chat_id=query.message.chat.id, 
            photo=product.photo.url,  # Telegram сам завантажить фото за посиланням
            caption=text
        )
    else:
        # Якщо у товару немає фото
        await bot.send_message(
            chat_id=query.message.chat.id, 
            text=text
        )
else:
    await bot.send_message(
        query.message.chat.id,
        text="Unfortunately, there are no products in this subcategory 🙁",
        reply_markup=markup,
    )


async def show_subcategories(query: types.CallbackQuery):
    if sign_in['current_state']:
        elem = query.data.split(':')
        if await category_subcategory_exists(subcategory_category_id=elem[1]):
            await query.answer(text="SubCategories")
            await bot.send_message(
                chat_id=query.message.chat.id,
                text="Please choose a subcategory from the list ☺️",
                reply_markup=await get_subcategories(elem[1]),
            )
        else:
            await bot.send_message(
                chat_id=query.message.chat.id,
                text="Sorry, there are no products in this category 😔",
                reply_markup=markup,
            )
    else:
        await bot.send_message(
            chat_id=query.message.chat.id,
            text="You are not logged in, please try logging into your profile ‼️",
            reply_markup=sign_inup_kb.markup,
        )


async def show_products(query: types.CallbackQuery):
    if sign_in['current_state']:
        await query.answer("Product Catalog")
        await get_products(query)
    else:
        await bot.send_message(
            chat_id=query.message.chat.id,
            text="You are not logged in, please try logging into your profile ‼️",
            reply_markup=sign_inup_kb.markup,
        )


@sync_to_async
def subcategory_products_exists(product_subcategory_id):
    return Product.objects.filter(product_subcategory=product_subcategory_id).exists()


@sync_to_async
def category_subcategory_exists(subcategory_category_id):
    return SubCategory.objects.filter(subcategory_category_id=subcategory_category_id).exists()


@sync_to_async
def category_exists():
    return Category.objects.all().exists()


def catalog_handlers_register():
    dp.register_message_handler(show_categories, Text(equals='Catalog 🛒'))
    dp.register_callback_query_handler(show_subcategories, category_cb.filter(action='view_categories'))
    dp.register_callback_query_handler(show_products, subcategory_cb.filter(action='view_subcategories'))

@sync_to_async
def get_subcategory_products_list(subcategory_id):
    return list(Product.objects.filter(product_subcategory_id=subcategory_id))

