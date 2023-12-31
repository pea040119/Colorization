model_name="lab_2"
model_type="best"
data_dir="/home/work/Circuit/dataset/"

python -m main.spixelseg.train_spixel --dataset custom --data_dir $data_dir --save_dir model/$model_name --exp_name spixel
python -m main.colorizer.train_colorizer --model AnchorColorProb --dataset custom --batch_size 16 --data_dir $data_dir --save_dir model/$model_name --ckpt_dir  model/$model_name/spixel/checkpts/model_$model_type.pth.tar --exp_name disco --dense_pos --enhanced