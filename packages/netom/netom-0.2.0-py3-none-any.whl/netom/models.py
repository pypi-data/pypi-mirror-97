from confu import schema


class BgpNeighbor(schema.Schema):
    """
    Defines the BGP Neighbor model.
    """

    name = schema.Str("name", help="name of the session")
    description = schema.Str(
        "description", help="description of the session", default=None
    )
    enabled = schema.Bool("enabled", help="enabled", default=True)
    neighbor_address = schema.IpAddress("neighbor_address", help="neighbor IP address")
    peer_as = schema.Int("peer_as", help="neighbor AS number")
    peer_group = schema.Str("peer_group", help="peer group")
    peer_type = schema.Str(
        "peer_type", help="peer type (internal or external)", default="external"
    )
    max_prefixes = schema.Int(
        "max_prefixes", help="maximum number of prefixes to accept"
    )
    import_policy = schema.Str("import_policy", help="Import policy to apply")
    export_policy = schema.Str("export_policy", help="Export policy to apply")
    auth_password = schema.Str(
        "auth_password", help="MD5 session password", default=None
    )
    local_address = schema.IpAddress(
        "local_address", help="local IP address", default=None
    )
    local_as = schema.Int("peer_as", help="neighbor AS number", default=0)
