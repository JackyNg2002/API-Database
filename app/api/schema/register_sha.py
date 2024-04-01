def reg_args_valid(parser):
    parser.add_argument('username', type=str, required=True, location='json')
    parser.add_argument('password', type=str, required=True, dest='pwd', location='json')
    parser.add_argument('email', type=str, required=True, location='json')
def log_args_valid(parser):
    parser.add_argument('username', type=str, required=True, location='json')
    parser.add_argument('password', type=str, required=True, dest='pwd', location='json')