from discord_webhook import DiscordWebhook, DiscordEmbed

def notify_new_listings(new_listings):
    webhook_url = 'YOUR_DISCORD_WEBHOOK_URL'  # Replace with your discord webhook

    if new_listings:
        print("New listings found!")
        for listing in new_listings:
            print(f"Title: {listing['title']}, Price: {listing['price']}, Link: {listing['link']}")
            
            # Create and send a Discord notification
            webhook = DiscordWebhook(url=webhook_url)
            embed = DiscordEmbed(title=listing['title'], description=f"Price: {listing['price']}\n[Link]({listing['link']})", color='03b2f8')
            embed.set_image(url=listing['img'])
            webhook.add_embed(embed)
            response = webhook.execute()
    else:
        print("No new listings found.")