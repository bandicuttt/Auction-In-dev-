from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from auctions.models.auctions import Auction, AuctionImage


@admin.register(Auction)
class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Auction Data', {
            'fields': (
                'title','description','start_time','end_time',
                'starting_price','current_price','seller_id',
                'winner_id',
           )
        }),
    )
    list_display = ('id', 'title','description','start_time','end_time',
                    'starting_price','current_price','status','seller_id',
                    'winner_id',)
    list_display_links = ('id',)
    ordering = ('-id',)

@admin.register(AuctionImage)
class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Auction Image Data', {
            'fields': (
                'auction',
                'image',
           )
        }),
    )
    list_display = ('id', 'auction','image',)
    list_display_links = ('id',)
    ordering = ('-id',)