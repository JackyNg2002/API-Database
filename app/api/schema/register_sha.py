def reg_args_valid(parser):
    parser.add_argument('username', type=str, required=True, location='json')
    parser.add_argument('password', type=str, required=True, dest='pwd', location='json')