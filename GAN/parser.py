from argparse import ArgumentParser
import configparser

parser = ArgumentParser()

#TODO: Split between GAN and VXM 

parser.add_argument("--config_file", type=str,
                    required=True,
                    help='Config file')

parser.add_argument('--epochs', type=int, 
                    default=200, 
                    help="Training epochs, default: 200")

parser.add_argument('--steps_per_epoch', type=int,
                    default=1000,
                    help="Number of steps per epoch")

parser.add_argument('--batch_size', type=int, 
                    default=1, 
                    help="training instances in each batch, default: 1")
# changed everything 
parser.add_argument('--dataset', type=str,
                    help="Path to dataset")
# changed name 
parser.add_argument('--prefix_name', type=str, 
                    default='VXM_ATLAS', 
                    help="Folder name where the data is saved")

parser.add_argument('--d_train_steps', type=int, 
                    default=1, 
                    help="Discriminator updates in each GAN cycle, default: 1")

parser.add_argument('--g_train_steps', type=int, 
                    default=1,
                    help="Generator updates in each GAN cycle, default: 1")

parser.add_argument('--lr_g', type=float, 
                    default=1e-4, 
                    help="Learning rate generator, default: 1e-4")

parser.add_argument('--lr_d', type=float, 
                    default=3e-4,
                    help="Learning rate discriminator, default: 3e-4")

parser.add_argument('--beta1_g', type=float, 
                    default=0.0,
                    help="Adam beta1 generator, default: 0.0")

parser.add_argument('--beta2_g', type=float,
                    default=0.9,
                    help="Adam beta2 generator, default: 0.9")

parser.add_argument('--beta1_d', type=float, 
                    default=0.0,
                    help="Adam beta1 discriminator, default: 0.0")

parser.add_argument('--beta2_d', type=float, 
                    default=0.9,
                    help="Adam beta2 discriminator default: 0.9")
# ???? 
parser.add_argument('--unconditional', 
                    dest='conditional', 
                    default=True, 
                    action='store_false', 
                    help="Train conditional/unconditional templates")

parser.add_argument('--nonorm_reg', type=bool,
                    dest='norm_reg', 
                    default=True, 
                    action='store_false',
                    help="""Instance normalization in registration branch, 
                    default: True""")

parser.add_argument('--oversample', type=bool, 
                    dest='oversample', 
                    default=True, 
                    action='store_false',
                    help="Oversample rare ages during training, default: True")

parser.add_argument('--d_snout', type=bool, 
                    dest='d_snout', 
                    default=False, 
                    action='store_true',
                    help="""Apply spectral norm to the last layer of the 
                    discriminator, default: False""")

parser.add_argument('--clip', type=bool, 
                    dest='clip_bckgnd', 
                    default=False, 
                    action='store_true',
                    help="""Clip the template background during training, 
                    default: False """)

parser.add_argument('--reg_loss', type=str, 
                    default='NCC', 
                    help="""Type of registration loss. 
                    One of {'NCC', 'NonSquareNCC'}, default: NCC""")
                    
parser.add_argument('--losswt_reg', type=float,
                    default=1.0,
                    help="Multiplier deformation regularizers, default: 1.0")

parser.add_argument('--losswt_gan', type=float, 
                    default=0.1, 
                    help="GAN loss weight in generator loss, default: 0.1")

parser.add_argument('--losswt_tv', type=float, 
                    default=0.00, 
                    help="""Weight of TV penalty on generated templates,
                    default:0.00""")

parser.add_argument('--losswt_gp', type=float, 
                    default=1e-3, 
                    help="Gradient penalty discriminator loss, default=1e-3")

parser.add_argument('--gen_config', type=str, 
                    default='ours',
                    help="""Template generator architecture. 
                    One of {'ours', 'voxelmorph'}, default: 'ours'""")
# changed name 
parser.add_argument('--seed', type=int, 
                    default=33,
                    help="Random seed to sort data, default: 33")

parser.add_argument('--start_step', type=int, 
                    default=0, 
                    help="Step to activate GAN training, default: 0")

parser.add_argument('--resume_ckpt', type=int, 
                    default=0, 
                    help="If >0 then resume training from given ckpt index")

parser.add_argument('--g_ch', type=int,
                    default=32, 
                    help="Channel width multiplier generator, default: 32")

parser.add_argument('--d_ch', type=int, 
                    default=64, 
                    help="Channel width multiplier discriminator, default: 64")

parser.add_argument('--init', type=str, 
                    default='default', 
                    help="""Weight initialization. 
                    One of {'default', 'orthogonal'}, default: 'default'""")

parser.add_argument('--lazy_reg', type=int,
                    default=1, 
                    help="""apply gradient penalty only once every lazy_reg 
                    iterations, default: 1""")

args = parser.parse_args()

#

if args.config_file:
    config = configparser.ConfigParser()
    config.read(args.config_file)
    defaults = {}
    defaults.update(dict(config.items("Defaults")))
    parser.set_defaults(**defaults)
    args = parser.parse_args() # Overwrite arguments