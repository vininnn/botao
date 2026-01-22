def display_author(embed, user):
    embed.set_author(
        name=user.display_name,
        icon_url=user.display_avatar.url
    )

    return embed