def validate_student_availability(interaction, private_Manager, server_Manager, public_Manager) -> None:
    """Validates the student's availability. It becomes valid if the student is not in any type of room or on any voice channel.

    Args:
        interaction: Interaction originating from Discord.
        privateRoomManager: PrivateRoomManager instance for validation.
        serverRoomManager : ServerRoomManager instance for validation.
        publicRoomManager : PublicRoomManager instance for validation.

    Raises:
        ValueError: If the student isn't in a voice channel.
        ValueError: If the student already has an active Private Study Room.
        ValueError: If the student already has an active Server Study Room.
        ValueError: If the student already has an active Public Study Room.
    """
    user_id = interaction.user.id

    if not interaction.user.voice or not interaction.user.voice.channel:
        raise ValueError('You need to be on a **voice channel** to open or join in a room.')

    if private_Manager.is_user_in_private_room(user_id):
        raise ValueError('You are currently in a Private Study Room! Close it first.')

    if server_Manager.is_user_in_server_room(user_id):
        raise ValueError('You are currently in a Server Study Room! Leave it first.')
    
    if public_Manager.is_user_in_public_room(user_id):
        raise ValueError('You are currently in a Public Study Room! Leave it first.')
    