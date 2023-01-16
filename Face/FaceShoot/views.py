import time

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect

# DB関係の参照
from django.utils import timezone

# テーブルとDBのフォーム読み込み
from FaceShoot.models import SimplePhoto, User
from FaceShoot.forms import SimplePhotoForm, UserForm

# 画像認識の参照
import shutil  # ファイル操作
import os  # OSのファイル操作
import glob  # ワイルドカードの操作
import cv2  # 顔認証ライブラリ
import numpy as np  # 画像の配列化
from PIL import Image  # ブラウザではなく、pythonの画像表示用

# MySQLの参照
import pymysql  # MySQL使う

# スマホURL
import qrcode


def learn_face(request, school_num=None):
    """顔データ登録"""
    print(school_num)
    # 定数定義
    ESC_KEY = 27  # Escキー
    INTERVAL = 33  # 待ち時間

    # ファイルがあるか判定してなければ作る
    if os.path.isdir('media/test'):
        print('テストフォルダOK')
    else:
        print('テストフォルダ作ります')
        os.mkdir('media/test')
    if os.path.isdir('media/face'):
        print('親フォルダOK')
    else:
        print('親フォルダ作ります')
        os.mkdir('media/face')
    if os.path.isdir('media/face/{}'.format(school_num)):
        print('学籍番号別のフォルダOK')
    else:
        print('学籍番号別のフォルダ作ります')
        os.mkdir('media/face/{}'.format(school_num))
    if os.path.isdir('media/face/{}/{}_study'.format(school_num, school_num)) and os.path.isdir(
            'media/face/{}/{}_disp'.format(school_num, school_num)):
        print('学籍番号別の学習フォルダと表示用フォルダOK')
    else:
        if os.path.isdir('media/face/{}/{}_study'.format(school_num, school_num)):
            print('学籍番号別の学習用フォルダOK')
        else:
            print('学籍番号別の学習用フォルダを作ります')
            os.mkdir('media/face/{}/{}_study'.format(school_num, school_num))
        if os.path.isdir('media/face/{}/{}_disp'.format(school_num, school_num)):
            print('学籍番号別の表示用フォルダOK')
        else:
            print('学籍番号別の表示用フォルダを作ります')
            os.mkdir('media/face/{}/{}_disp'.format(school_num, school_num))

    # フォルダ作成完了
    face_file_list = glob.glob('media/face/{}/{}_disp/**'.format(school_num, school_num))

    # 画像があれば処理を分ける
    training_image_flg = False
    if len(face_file_list) == 0:
        print('画像無し')
        training_image_flg = False
    else:
        print('画像ある')
        training_image_flg = True

    face_num = len(face_file_list)
    face_num = int(face_num) + 1
    print('画像の数： {}'.format(face_num))
    # print('出てほしい：{}'.format(face_num))

    print('番号出す')
    big_num_name = 0
    for number in face_file_list:
        next_num = number.split('_')[2].split('.')[0]
        # print(next_num)
        if big_num_name < int(next_num):
            big_num_name = int(next_num)

    print('欲しい番号: {}'.format(big_num_name))
    face_num = big_num_name + 1

    FACE_SIKAKU_NAME = "sikaku"  # カラー顔認証
    # 分類器の指定
    cascade_file = "templates/FaceShoot/haarcascade_frontalface_default.xml"
    cascade = cv2.CascadeClassifier(cascade_file)
    # カメラ映像取得
    cap = cv2.VideoCapture(0)
    # 初期フレームの読込
    end_flag, c_frame = cap.read()
    # ウィンドウの準備
    cv2.namedWindow(FACE_SIKAKU_NAME)
    # 結果出力用のパス
    kao = []

    # カウント関数
    j = 1
    end_flag = True

    # カメラ処理ループ
    while end_flag:
        # 画像の取得と顔の検出
        img = c_frame
        img_face = c_frame
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_list = cascade.detectMultiScale(img_gray, minSize=(100, 100))

        # 検出した顔に印を付ける
        for (x, y, w, h) in face_list:
            color = (0, 0, 225)
            pen_w = 3
            cv2.rectangle(img_gray, (x, y), (x + w, y + h), color, thickness=pen_w)
            cv2.rectangle(img_face, (x, y), (x + w, y + h), color, thickness=pen_w)

        # フレーム表示
        cv2.imshow(FACE_SIKAKU_NAME, img_face)

        # 顔があれば写真保存
        if face_list is not None and len(face_list) > 0:
            Face_Img = img_gray
            # キーボード入力待ち
            key = cv2.waitKey(1) & 0xFF
            if key == ord('s'):

                # 顔部分を切り取る
                for x, y, w, h in face_list:
                    face_cut = img[y:y + h, x:x + w]
                    Face_Img = face_cut
                    ColorFaceImage = face_cut
                    # グレースケール化
                    Face_Img = cv2.cvtColor(Face_Img, cv2.COLOR_BGR2GRAY)

                # 顔を保存する
                view_path = "media/face/{}/{}_disp/{}_{}.jpg".format(school_num, school_num, school_num, face_num)
                lean_path = "media/face/{}/{}_study/{}.{}.jpg".format(school_num, school_num, school_num, face_num)
                test_path = 'media/test/{}_{}.jpg'.format(school_num, face_num)

                # 顔のパスに追加
                kao.append(view_path)

                # 閲覧用と学習用に二つ保存する
                cv2.imwrite(view_path, ColorFaceImage)

                # 初回は訓練画像として保存する
                if training_image_flg:
                    print(training_image_flg)
                    print('判定するのでテスト画像')
                    cv2.imwrite(test_path, Face_Img)
                    rename = 'media/test/{}.{}'.format(school_num, face_num)
                    os.rename(test_path, rename)
                # 次回からはテスト画像として保存する
                else:
                    print(training_image_flg)
                    print('初回なので訓練画像')
                    cv2.imwrite(lean_path, Face_Img)
                    rename = 'media/face/{}/{}_study/{}.{}'.format(school_num, school_num, school_num, face_num)
                    os.rename(lean_path, rename)

                if face_num > 100:
                    print('コンプリート')
                    break
                else:
                    face_num = face_num + 1
                    print('カウント：{}'.format(face_num))

        # Escキーで終了
        key = cv2.waitKey(INTERVAL)
        if key == ESC_KEY:
            break

        # 次のフレーム読み込み
        end_flag, c_frame = cap.read()

    # 終了処理
    cv2.destroyAllWindows()
    cap.release()

    print('出せ: {}'.format(school_num))
    school_num = school_num

    """顔の画像を表示したい"""
    return render(request,
                  'FaceShoot/user_face.html',  # 使用するテンプレート
                  {'kao': kao, 'school_num': school_num, 'flg': training_image_flg})  # テンプレートに渡すデータ


def picture_list(request):
    """カメラ起動"""
    cap = cv2.VideoCapture(0)
    path = 'media/img.jpg'
    while True:
        # フレームをキャプチャする
        ret, frame = cap.read()
        # 画面に表示する
        cv2.imshow('frame', frame)
        # キーボード入力待ち
        key = cv2.waitKey(1) & 0xFF
        # qが押された場合は終了する
        if key == ord('q'):
            break
        # sが押された場合は保存する
        if key == ord('s'):
            cv2.imwrite(path, frame)
            print(path)
            break

    # キャプチャの後始末と，ウィンドウをすべて消す
    cap.release()
    cv2.destroyAllWindows()

    """確認画面"""
    return render(request, 'FaceShoot/picture.html', {'pics': path})


def ninsyo(req):
    """顔認証で出勤"""
    old = time.time()  # 読み込みにかかった時間
    print('読み込み時間: ', end='', flush=True)
    cascadePath = 'templates/FaceShoot/haarcascade_frontalface_default.xml'
    faceCascade = cv2.CascadeClassifier(cascadePath)
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    # 自作の分類器読み込み
    recognizer.read('templates/FaceShoot/face_recognizer.xml')
    loading_time = time.time() - old
    loading_time = str(loading_time).split('.')[0] + '.' + str(loading_time).split('.')[1][1]
    print(loading_time, '秒')
    cap = cv2.VideoCapture(0)
    # 文字のフォント設定
    font = cv2.FONT_HERSHEY_PLAIN
    # 文字のサイズ設定
    font_size = 5
    # 結果
    how_Mach = 0
    login_Number = 0

    while True:
        # フレームの取得
        ret, frame = cap.read()
        if ret:
            # Webカメラからの画像を白黒画像として読み込み
            image_pil = 299 / 1000 * frame[:, :, 0] + 587 / 1000 * frame[:, :, 1] + 114 / 1000 * frame[:, :, 2]
            image = np.array(image_pil, 'uint8')
            # Haar-like特徴分類器で顔を検知
            image1 = faceCascade.detectMultiScale(image)
            if len(image1) > 0:
                x, y, w, h = image1[0][0], image1[0][1], image1[0][2], image1[0][3]
                # 200×200にリサイズ
                image2 = cv2.resize(image[y: y + h, x: x + w], (200, 200), interpolation=cv2.INTER_LINEAR)
                # 類似度を予測
                label, predict_Confidence = recognizer.predict(image2)
                # 類似度を画面に表示
                cv2.putText(frame, str(predict_Confidence), (50, 700), font, font_size, (255, 255, 0), 4)
                cv2.imshow('Show', frame)

                print('類似度： {}'.format(int(predict_Confidence)))
                print('似ている画像： {}'.format(label))
                if 30 < predict_Confidence < 100:
                    print('50％以上なので認証成功！！ ：{}'.format(int(predict_Confidence)))
                    how_Mach = int(predict_Confidence)
                    login_Number = label
                    break
            # 1msecキー入力待ち
            cv2.waitKey(1)
        else:
            break
    # 終了処理
    cv2.destroyAllWindows()
    cap.release()

    user = User.objects.get(schoolnum=login_Number)

    # 日付取得
    in_year = timezone.datetime.now().year  # 年
    in_month = timezone.datetime.now().month  # 月
    in_day = timezone.datetime.now().day  # 日
    in_hour = timezone.datetime.now().hour  # 時間
    in_minute = timezone.datetime.now().minute  # 分

    # 日付と時間
    today = '{}/{}/{} {}:{}'.format(in_year, in_month, in_day, in_hour, in_minute)
    print(today)

    return render(req,
                  'FaceShoot/face_pass.html',
                  {'mach': how_Mach,
                   'school_num': login_Number,
                   'user': user,
                   'loading_time': loading_time})


def imagelist(req):
    """DBの画像を取得"""
    images = SimplePhoto.objects.all()
    if req.method == 'POST':
        form = SimplePhotoForm(req.POST, req.FILES)
        if form.is_valid():
            form.save()
    else:
        form = SimplePhotoForm()

    return render(req, 'FaceShoot/imagelist.html', {'images': images, 'form': form})


def user_disp(req):
    """ユーザー一覧"""
    users = User.objects.all().order_by('id')
    return render(req, 'FaceShoot/user_disp.html', {'users': users})


def user_edit(req, user_id=None):
    """ユーザーの編集"""
    if user_id:  # user_id が指定されている (修正時)
        user = get_object_or_404(User, schoolnum=user_id)
    else:  # user_id が指定されていない (追加時)
        user = User()

    if req.method == 'POST':
        form = UserForm(req.POST, instance=user)  # POST された request データからフォームを作成
        if form.is_valid():  # フォームのバリデーション
            user = form.save(commit=False)
            user.save()
            return redirect('FaceShoot:user_disp')
    else:  # GET の時
        form = UserForm(instance=user)  # user インスタンスからフォームを作成

    return render(req, 'FaceShoot/user_edit.html', dict(form=form, user_id=user_id))


def user_del(req, user_id=None):
    """ユーザーの削除"""
    user = get_object_or_404(User, schoolnum=user_id)
    print(user)
    print(user_id)
    user.delete()
    # 後処理で作ったディレクトリを掃除する
    shutil.rmtree('media/face/{}'.format(user_id))
    print('学習したフォルダの削除完了')
    users = User.objects.all().order_by('id')
    return render(req, 'FaceShoot/user_disp.html', {'users': users})


def login(req, user_id=None):
    """ユーザー情報"""
    print('ログイン開始')
    try:
        login_key = ''
        users = []
        sessin_id = ''
        searchErrMsg = ''
        File = []
        print('セッション調教')
        if user_id:
            print(user_id)
            # login_key = req.POST['txtGakuseki']
            login_key = user_id
            if User.objects.get(schoolnum=login_key):
                users = User.objects.get(schoolnum=login_key)
                print(users.user_name)
            else:
                searchErrMsg = '見つかりませんでした。もう一度入力してください'
            if users.user_name:
                print('認証成功')
                # セッションにIDとして保存
                req.session['id'] = user_id
                sessin_id = req.session['id']
                print('セッション：{}'.format(sessin_id))
                if 'id' in req.session:
                    print('セッション成功')
                    req.session.set_expiry(0)  # 有効期限：ブラウザ閉じるまで
                    print('キー出せ：{}'.format(req.session.keys()))
                    print('ID出せ：{}'.format(req.session.get('id')))

                    # 顔画像ファイルがあるか判定
                    if os.path.isdir('media/face'):
                        # あればスルー
                        if os.path.isdir('media/face'):
                            print('フォルダ検査OK')
                            print('ファイル検査開始')
                            # 対象のフォルダ
                            File = glob.glob('media/face/{}/{}_disp/**'.format(sessin_id, sessin_id))
                            print('フォルダ一覧：{}'.format(File))

    except KeyError:
        print('そんな名前の変数はない')
        pass
    except ObjectDoesNotExist:
        print('検索失敗')
        pass
    except UnboundLocalError:
        print('定義前に変数が使用された')
        pass

    return render(req, 'FaceShoot/loginform.html',
                  {'Gakuseki': login_key,
                   'searchErrMsg': searchErrMsg,
                   'user': users,
                   'session_id': sessin_id,
                   'kao': File})


def get_image(req):
    """学習済み顔画像取得"""
    Folder = os.path.isdir("media/face/")
    File = glob.glob("media/face/**")
    print('ディレクトリの確認：media/face/{}'.format(Folder))
    print('ファイルの確認：media/face/ 画像(list):{}'.format(File))
    # 人数カウント
    count = 1
    # 画像が欲しい
    key = 'disp'
    # 親フォルダ
    folderlist = []
    # サブフォルダ
    foldername_gakuseki = []
    # 目的の取得したい学習用のファイル一覧
    doublefolderlist = []
    # 特定の学籍番号のフォルダ
    students_folder = []
    # 取得したファイルパスリスト
    get_file_path = []

    # フォルダかあれば開始
    if os.path.isdir("media/face/"):
        print('検査開始')
        for facefiles in glob.glob("media/face/**"):
            print('親フォルダ：{}'.format(facefiles))
            if facefiles:
                folderlist.append(facefiles)
        # サブフォルダがあればフォルダ名を取得する
        if folderlist:
            print('学籍番号のフォルダ：{}'.format(folderlist))
            # サブフォルダ名の取得を試みる
            for foldername in folderlist:
                print('学籍番号別のフォルダ：{}'.format(foldername.split('\\')[1]))
                foldername_gakuseki.append(foldername.split('\\')[1])
            if foldername_gakuseki:
                print('学籍番号別のフォルダリスト：{}'.format(foldername_gakuseki))
                for doublefolder in foldername_gakuseki:
                    if doublefolder:
                        # 学籍別の二つのフォルダパスを取得
                        gakuseki_folder = glob.glob('media/face/{}/**'.format(doublefolder))
                        print('学習用と表示用のフォルダ：{}'.format(doublefolderlist))
                        # 収納
                        doublefolderlist.append(gakuseki_folder)
                # 表示用か学習用かで分岐
                if doublefolderlist:
                    print('切り分け前：{}'.format(doublefolderlist))
                    for students_number in doublefolderlist:
                        print('切り分け後：{}'.format(students_number))
                        students_folder.append(students_number)
                    # ここから学籍番号で絞り込み
                    if students_folder:
                        print('学籍番号別にリストに格納：{}'.format(students_folder))
                        for student_forcus in students_folder:
                            print('{}人目：{}'.format(count, student_forcus))
                            if student_forcus:
                                for bothfolder in student_forcus:
                                    print('どっちかが欲しい：{}'.format(bothfolder))
                                    authority_key = bothfolder.split('_')[1]
                                    print('選択キー：{}'.format(authority_key))
                                    # 画像ファイルか学習ファイルを取得
                                    if key == authority_key:
                                        resultfile = glob.glob('{}/**'.format(bothfolder))
                                        print(resultfile)
                                        get_file_path.append(resultfile)
                            # 人数カウント
                            count = count + 1
    print('画像の全件取得：{}'.format(get_file_path))

    return render(req,
                  'FaceShoot/getfile.html',
                  {'get_file_path': get_file_path})


def user_face_learn(req, user_id):
    """顔学習"""
    Folder = os.path.isdir("media/face/")
    File = glob.glob("media/face/**")

    print('ディレクトリの確認：{}'.format(Folder))
    print('ファイルの確認：{}'.format(File))

    # ファイルがあるか判定
    if os.path.isdir('media/face/training_folder'):
        print('検証フォルダが消えてないので再生成')
        shutil.rmtree('media/face/training_folder')
        os.mkdir('media/face/training_folder')
    else:
        print('検証フォルダ作ります')
        os.mkdir('media/face/training_folder')

    # 人数カウント
    count = 1

    # 訓練画像が欲しい
    key = 'study'

    # 親フォルダ
    folderlist = []
    # サブフォルダ
    foldername_gakuseki = []
    # 目的の取得したい学習用のファイル一覧
    doublefolderlist = []
    # 特定の学籍番号のフォルダ
    students_folder = []
    # 取得したファイルパスリスト
    get_file_path = []
    # 学習用のフォルダーを取得
    get_study_folder = []

    # フォルダかあれば開始
    if os.path.isdir("face/"):
        print('-------------------検査開始--------------------------------')
        for facefiles in glob.glob("media/face/**"):
            print('親フォルダ：{}'.format(facefiles))
            if facefiles:
                folderlist.append(facefiles)
        # サブフォルダがあればフォルダ名を取得する
        if folderlist:
            print('学籍番号のフォルダ：{}'.format(folderlist))
            # サブフォルダ名の取得を試みる
            for foldername in folderlist:
                print('学籍番号別のフォルダ：{}'.format(foldername.split('\\')[1]))
                foldername_gakuseki.append(foldername.split('\\')[1])
            if foldername_gakuseki:
                print('学籍番号別のフォルダリスト：{}'.format(foldername_gakuseki))
                for doublefolder in foldername_gakuseki:
                    if doublefolder:
                        # 学籍別の二つのフォルダパスを取得
                        gakuseki_folder = glob.glob('media/face/{}/**'.format(doublefolder))
                        print('学習・表示：{}'.format(doublefolderlist))
                        # 収納
                        doublefolderlist.append(gakuseki_folder)
                # 表示用か学習用かで分岐
                if doublefolderlist:
                    print('両方：{}'.format(doublefolderlist))
                    for students_number in doublefolderlist:
                        print('切り分ける：{}'.format(students_number))
                        students_folder.append(students_number)
                    # ここから学籍番号で絞り込み
                    if students_folder:
                        print('学籍番号別：{}'.format(students_folder))
                        for student_forcus in students_folder:
                            print('{}人目：{}'.format(count, student_forcus))
                            if student_forcus:
                                for bothfolder in student_forcus:
                                    # print('どっちかが欲しい：{}'.format(bothfolder))
                                    authority_key = bothfolder.split('_')[1]
                                    # print('選択キー：{}'.format(authority_key))
                                    # 画像ファイルか学習ファイルを取得
                                    if key == authority_key:
                                        # print('学習用フォルダ：{}'.format(bothfolder))
                                        get_study_folder.append(bothfolder)
                                        resultfile = glob.glob('{}/**'.format(bothfolder))
                                        # print(resultfile)
                                        get_file_path.append(resultfile)
                            # 人数カウント
                            count = count + 1

    print('---------------------------------検査終了---------------------------------')
    print('学習ファイル一覧：{}'.format(get_file_path))
    print('取得したフォルダ：{}'.format(get_study_folder))
    print('-------------------一覧から訓練フォルダ作成-------------------------------')
    for dekita in get_study_folder:
        print('コピーするフォルダ：{}'.format(dekita))
        # フォルダ内のファイルをひとつずつコピー
        for files in os.listdir(dekita):
            # ファイルコピーの開始
            shutil.copy(os.path.join(dekita, files), 'media/face/training_folder/')
            # print('コピー：{}'.format(files))

    # 学習用データを読み込むフォルダができた
    print('------------------------顔認証エリア-----------------------')
    send_file = glob.glob('media/face/training_folder/**')
    print('訓練フォルダ確認：{}'.format(send_file))

    # 特定の人物で学習
    train_path = r'C:\Users\minor\PycharmProjects\face\media\face\training_folder'
    test_path = r'C:\Users\minor\PycharmProjects\face\media\test'

    mach_file = glob.glob(r'{}\**'.format('media/face/training_folder'))
    print('ファイル一覧：{}'.format(mach_file))
    print('ファイル数：{}'.format(len(mach_file)))

    # Haar-like特徴分類器
    cascadePath = r'C:\Users\minor\PycharmProjects\Face\templates\FaceShoot\haarcascade_frontalface_default.xml'
    faceCascade = cv2.CascadeClassifier(cascadePath)

    # 顔認識器の構築
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    # 指定されたpath内の画像を取得
    def get_images_and_labels(path):
        # 画像を格納する配列
        images = []
        # ラベルを格納する配列
        labels = []
        # ファイル名を格納する配列
        files = []
        print('取得先： {}'.format(path))
        for f in os.listdir(path):
            # 上と下のpathで取得先の変換なし
            # print('取得先： {}'.format(path))
            # 画像のパス
            image_path = os.path.join(path, f)
            # print(image_path)
            # グレースケールで画像を読み込む
            image_pil = Image.open(image_path).convert('L')
            # NumPyの配列に格納
            image = np.array(image_pil, 'uint8')
            # Haar-like特徴分類器で顔を検知
            faces = faceCascade.detectMultiScale(image)
            # 検出した顔画像の処理
            for (x, y, w, h) in faces:
                # 顔を 200x200 サイズにリサイズ
                roi = cv2.resize(image[y: y + h, x: x + w], (200, 200), interpolation=cv2.INTER_LINEAR)
                # 画像を配列に格納
                images.append(roi)
                # ファイル名からラベルを取得
                print('画像：{}'.format(f))
                FaceLabel = f.split('_')[0]
                FaceLabel = FaceLabel.split('.')[0]

                # labels.append(int(f.split('.')[0][len(f.split('.')[0])-2:]))
                labels.append(int(FaceLabel))

                # ファイル名を配列に格納
                files.append(f)

        return images, labels, files

    # トレーニング画像を取得
    images, labels, files = get_images_and_labels(train_path)

    # トレーニング実施
    recognizer.train(images, np.array(labels))

    # テスト画像を取得
    test_images, test_labels, test_files = get_images_and_labels(test_path)

    print('-------------------------作成したフォルダ確認--------------------------')
    # print('テスト画像[配列]：{}'.format(test_images))
    print('テスト画像の番号：{}'.format(test_labels))
    print('テスト画像のフォルダ：{}'.format(test_path))
    print('テスト画像：{}'.format(test_files))
    print('訓練フォルダ： {}'.format(train_path))
    print('学習済画像のラベル： {}'.format(labels))
    print('-------------------------判別処理開始--------------------------')

    # 結果収納変数
    i = 0  # 判別した画像の枚数
    ans = []  # 辞書型の収納になる
    while i < len(test_labels):
        # テスト画像に対して予測実施
        label, confidence = recognizer.predict(test_images[i])
        # 予測結果をコンソール出力
        print("テスト画像: {}, 近い画像: {}, 的中率: {}".format(test_files[i], label, int(confidence)))
        # 結果を保存
        result_Set = {'Img': test_files[i], 'near': label, 'mach': int(confidence)}
        ans.append(result_Set)

        # テスト画像を表示
        # plt.imshow(test_images[i])
        # cv2.imshow("test image", test_images[i])
        # cv2.waitKey(300)

        i += 1

    # print('考察')
    # print('{} フォルダの画像の数だけ, {} フォルダの画像と比較予想を実施している'.format(test_path,train_path))
    # print('画像の名前の数字の部分をラベル変数で似ている画像の結果表示に使用している')
    # print('plt:プロットはループ処理中であっても複数動作せずプログラム終了時の一回のみ表示している')

    # 終了処理
    recognizer.write(r'templates\FaceShoot\face_recognizer.xml')  # 学習結果をファイルに書き込み
    cv2.destroyAllWindows()
    print('------------------------顔認証処理終了--------------------------')

    # 学習済みへ移動する前準備
    print('学習済みへ移動：{}'.format(test_path))
    copyFile = 'media/face/{}/{}_study/'.format(user_id, user_id)
    get_study_folder = os.listdir(test_path)

    # コピー先にのフォルダにパスを通すために前準備
    for file_name in get_study_folder:
        full_file_name = os.path.join(test_path, file_name)
        # フォルダ内のファイルをひとつずつコピー
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, copyFile)
            # print('コピー：{}'.format(full_file_name))
    # 後処理で作ったディレクトリを掃除する
    shutil.rmtree('media/test/')
    shutil.rmtree('media/face/training_folder/')
    print('一時的に作成したフォルダの掃除完了')

    return render(req, 'FaceShoot/personal_face_study_result.html', {'ans': ans})


def mysql_disp(req):
    """MySQLの実験①一覧"""
    # 接続情報
    dbh = pymysql.connect(
        host='localhost',  # ローカルのDB
        user='root',  # MySQL:ユーザ名
        password='root',  # MySQL:パスワード
        db='django_db',  # MySQL:ＤＢの名前
        charset='utf8',  # 文字コード(日本語)
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with dbh.cursor():
            stmt = dbh.cursor()  # カーソル
            sql = "SELECT * FROM t_user"
            stmt.execute(sql)
            print(stmt._executed)  # ＳＱＬ文確認
            query_set = stmt.fetchall()  # 結果を収納
    finally:
        # お掃除
        stmt.close()
        dbh.close()

    return render(req,
                  'FaceShoot/mysql-disp.html',
                  {'query_set': query_set})


def search(req):
    """MySQLの実験②検索"""
    schoolnum = req.POST['schoolnum']
    name = req.POST['name']
    create_at = req.POST['create_at']
    # 入力されたデータを表示する
    print(' schoolnum:{}\n name:{}\n create_at:{}'.format(schoolnum, name, create_at))
    # 接続情報
    dbh = pymysql.connect(
        host='localhost',  # ローカルのDB
        user='root',  # MySQL:ユーザ名
        password='root',  # MySQL:パスワード
        db='django_db',  # MySQL:ＤＢの名前
        charset='utf8',  # 文字コード(日本語)
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with dbh.cursor():
            stmt = dbh.cursor()  # カーソル
            sql = " select * from t_user "
            # ここからSQL文の組み立てを行う
            # 以下のSQL文では入力された項目についてそれぞれエスケープ処理をしている
            if schoolnum and name and create_at:
                sql += " where schoolnum like %(schoolnum)s and name like %(name)s and create_at like %(create_at)s "
                stmt.execute(sql,
                             {'schoolnum': '%' + schoolnum + '%',
                              'name': '%' + name + '%',
                              'create_at': '%' + create_at + '%'})
            elif schoolnum or name or create_at:
                sql += " where "
                if schoolnum:
                    sql += " schoolnum like %(schoolnum)s "
                    if name:
                        sql += " and name like %(name)s "
                        stmt.execute(sql, {'schoolnum': '%' + schoolnum + '%', 'name': '%' + name + '%'})
                    elif create_at:
                        sql += " and create_at like %(create_at)s "
                        stmt.execute(sql, {'schoolnum': '%' + schoolnum + '%', 'create_at': '%' + create_at + '%'})
                    else:
                        stmt.execute(sql, {'schoolnum': '%' + schoolnum + '%'})
                elif name:
                    sql += " name like %(name)s "
                    if create_at:
                        sql += " and create_at like %(create_at)s "
                        stmt.execute(sql, {'name': '%' + name + '%', 'create_at': '%' + create_at + '%'})
                    else:
                        stmt.execute(sql, {'name': '%' + name + '%'})
                elif create_at:
                    sql += " create_at like %(create_at)s "
                    stmt.execute(sql, {'create_at': '%' + create_at + '%'})
            else:
                stmt.execute(sql)

            print(stmt._executed)  # ＳＱＬ文確認
            query_set = stmt.fetchall()  # 結果を収納

    finally:
        # お掃除
        stmt.close()
        dbh.close()

    return render(req,
                  'FaceShoot/mysql-disp.html',
                  {'query_set': query_set})


def mysql_add(req):
    return render(req, 'FaceShoot/mysql-add.html')


def mysql_insert(req):
    schoolnum = req.POST['schoolnum']
    name = req.POST['name']
    password = req.POST['password']
    freetext = req.POST['freetext']
    print(' schoolnum:{}\n name:{}\n password:{}\n password:{}'.format(schoolnum, name, password, freetext))

    # 日付取得
    in_year = timezone.datetime.now().year
    in_month = timezone.datetime.now().month
    in_day = timezone.datetime.now().day
    today = '{}/{}/{}'.format(in_year, in_month, in_day)
    print(in_year, in_month, in_day)
    print(today)

    dbh = pymysql.connect(
        host='localhost',  # ローカルのDB
        user='root',  # MySQL:ユーザ名
        password='root',  # MySQL:パスワード
        db='django_db',  # MySQL:ＤＢの名前
        charset='utf8',  # 文字コード(日本語)
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with dbh.cursor():
            stmt = dbh.cursor()  # カーソル
            sql = "INSERT INTO t_user VALUES (%(schoolnum)s, %(name)s, %(password)s, %(freetext)s, %(date)s)"
            stmt.execute(sql, {'schoolnum': schoolnum,
                               'name': name,
                               'password': password,
                               'freetext': freetext,
                               'date': today})
            print(stmt._executed)  # ＳＱＬ文確認
            # 忘れたら動かないもの
            dbh.commit()

            stmt = dbh.cursor()  # カーソル
            sql = "SELECT * FROM t_user"
            stmt.execute(sql)
            print(stmt._executed)  # ＳＱＬ文確認
            query_set = stmt.fetchall()  # 結果を収納
    finally:
        # お掃除
        stmt.close()
        dbh.close()
    return render(req, 'FaceShoot/mysql-disp.html', {'query_set': query_set})


def mysql_update(req, schoolnum=None):
    # 接続情報
    dbh = pymysql.connect(
        host='localhost',  # ローカルのDB
        user='root',  # MySQL:ユーザ名
        password='root',  # MySQL:パスワード
        db='django_db',  # MySQL:ＤＢの名前
        charset='utf8',  # 文字コード(日本語)
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with dbh.cursor():
            stmt = dbh.cursor()  # カーソル
            sql = "SELECT * FROM t_user where schoolnum = %(schoolnum)s"
            stmt.execute(sql, {'schoolnum': schoolnum})
            print(stmt._executed)  # ＳＱＬ文確認
            query_set = stmt.fetchall()  # 結果を収納
    finally:
        # お掃除
        stmt.close()
        dbh.close()
    return render(req, 'FaceShoot/mysql_update.html', {'query_set': query_set})


def mysql_update_commit(req):
    # 接続情報
    print(req.POST)
    schoolnum = req.POST['schoolnum']
    name = req.POST['name']
    password = req.POST['password']
    freetext = req.POST['freetext']
    print('学籍番号：{}/名前：{}/パスワード：{}/テキスト：{}'.format(schoolnum, name, password, freetext))
    dbh = pymysql.connect(
        host='localhost',  # ローカルのDB
        user='root',  # MySQL:ユーザ名
        password='root',  # MySQL:パスワード
        db='django_db',  # MySQL:ＤＢの名前
        charset='utf8',  # 文字コード(日本語)
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with dbh.cursor():
            stmt = dbh.cursor()  # カーソル
            sql = ''
            # updateの条件文コネコネ
            if schoolnum and name and password and freetext:
                sql += ' UPDATE t_user SET '
                sql += ' schoolnum=%(schoolnum)s, name=%(name)s, password=%(password)s, freetext=%(freetext)s '
                sql += ' WHERE schoolnum=%(schoolnum_where)s '
                stmt.execute(sql,
                             {'schoolnum': schoolnum,
                              'name': name,
                              'password': password,
                              'freetext': freetext,
                              'schoolnum_where': schoolnum})
                dbh.commit()

            stmt = dbh.cursor()  # カーソル
            sql = " SELECT * FROM t_user "
            stmt.execute(sql)
            print(stmt._executed)  # ＳＱＬ文確認
            query_set = stmt.fetchall()  # 結果を収納
    finally:
        # お掃除
        stmt.close()
        dbh.close()
    return render(req, 'FaceShoot/mysql-disp.html', {'query_set': query_set})


def mysql_del(req, schoolnum=None):
    # 接続情報
    dbh = pymysql.connect(
        host='localhost',  # ローカルのDB
        user='root',  # MySQL:ユーザ名
        password='root',  # MySQL:パスワード
        db='django_db',  # MySQL:ＤＢの名前
        charset='utf8',  # 文字コード(日本語)
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with dbh.cursor():
            stmt = dbh.cursor()  # カーソル
            sql = "SELECT * FROM t_user where schoolnum = %(schoolnum)s"
            stmt.execute(sql, {'schoolnum': schoolnum})
            print(stmt._executed)  # ＳＱＬ文確認
            query_set = stmt.fetchall()  # 結果を収納
            print(query_set)
    finally:
        # お掃除
        stmt.close()
        dbh.close()
    return render(req, 'FaceShoot/mysql-del.html', {'query_set': query_set})


def mysql_delete_commit(req, schoolnum=None):
    print(schoolnum)
    dbh = pymysql.connect(
        host='localhost',  # ローカルのDB
        user='root',  # MySQL:ユーザ名
        password='root',  # MySQL:パスワード
        db='django_db',  # MySQL:ＤＢの名前
        charset='utf8',  # 文字コード(日本語)
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with dbh.cursor():
            stmt = dbh.cursor()  # カーソル
            sql = ' delete from t_user where schoolnum=%(schoolnum)s '
            stmt.execute(sql, {'schoolnum': schoolnum})
            print(stmt._executed)  # ＳＱＬ文確認
            dbh.commit()

            stmt = dbh.cursor()  # カーソル
            sql = "SELECT * FROM t_user "
            stmt.execute(sql)
            print(stmt._executed)  # ＳＱＬ文確認
            query_set = stmt.fetchall()  # 結果を収納
    finally:
        # お掃除
        stmt.close()
        dbh.close()
    return render(req, 'FaceShoot/mysql-disp.html', {'query_set': query_set})


def imgdel(req):
    # 顔認証のノイズになる画像の削除
    for item in req.POST.getlist('del_img'):
        print(item)
        os.remove(item)

    Folder = os.path.isdir("media/face/")
    File = glob.glob("media/face/**")
    print('ディレクトリの確認：media/face/{}'.format(Folder))
    print('ファイルの確認：media/face/ 画像(list):{}'.format(File))
    # 人数カウント
    count = 1
    # 画像が欲しい
    key = 'disp'
    # 親フォルダ
    folderlist = []
    # サブフォルダ
    foldername_gakuseki = []
    # 目的の取得したい学習用のファイル一覧
    doublefolderlist = []
    # 特定の学籍番号のフォルダ
    students_folder = []
    # 取得したファイルパスリスト
    get_file_path = []

    # フォルダかあれば開始
    if os.path.isdir("media/face/"):
        print('検査開始')
        for facefiles in glob.glob("media/face/**"):
            print('親フォルダ：{}'.format(facefiles))
            if facefiles:
                folderlist.append(facefiles)
        # サブフォルダがあればフォルダ名を取得する
        if folderlist:
            print('学籍番号のフォルダ：{}'.format(folderlist))
            # サブフォルダ名の取得を試みる
            for foldername in folderlist:
                print('学籍番号別のフォルダ：{}'.format(foldername.split('\\')[1]))
                foldername_gakuseki.append(foldername.split('\\')[1])
            if foldername_gakuseki:
                print('学籍番号別のフォルダリスト：{}'.format(foldername_gakuseki))
                for doublefolder in foldername_gakuseki:
                    if doublefolder:
                        # 学籍別の二つのフォルダパスを取得
                        gakuseki_folder = glob.glob('media/face/{}/**'.format(doublefolder))
                        print('学習用と表示用のフォルダ：{}'.format(doublefolderlist))
                        # 収納
                        doublefolderlist.append(gakuseki_folder)
                # 表示用か学習用かで分岐
                if doublefolderlist:
                    print('切り分け前：{}'.format(doublefolderlist))
                    for students_number in doublefolderlist:
                        print('切り分け後：{}'.format(students_number))
                        students_folder.append(students_number)
                    # ここから学籍番号で絞り込み
                    if students_folder:
                        print('学籍番号別にリストに格納：{}'.format(students_folder))
                        for student_forcus in students_folder:
                            print('{}人目：{}'.format(count, student_forcus))
                            if student_forcus:
                                for bothfolder in student_forcus:
                                    print('どっちかが欲しい：{}'.format(bothfolder))
                                    authority_key = bothfolder.split('_')[1]
                                    print('選択キー：{}'.format(authority_key))
                                    # 画像ファイルか学習ファイルを取得
                                    if key == authority_key:
                                        resultfile = glob.glob('{}/**'.format(bothfolder))
                                        print(resultfile)
                                        get_file_path.append(resultfile)
                            # 人数カウント
                            count = count + 1
    print('画像の全件取得：{}'.format(get_file_path))

    # 削除後の結果を返す
    return render(req,
                  'FaceShoot/getfile.html',
                  {'get_file_path': get_file_path})


def user_face_del(req):
    user_id = req.POST.getlist('user_id')[0]
    all_face = req.POST.getlist('all_face')
    print('今回撮影した画像: {}'.format(all_face))
    # 顔認証のノイズになる画像の削除
    for item in req.POST.getlist('del_img'):
        print('削除画像: {}'.format(item))
        # 画像ナンバー抜き出し
        img_Number = item.split('_')[2].split('.')[0]
        # 訓練画像に対応する画像があるか
        study = 'media/face/{}/{}_study/{}.{}'.format(user_id, user_id, user_id, img_Number)
        disp = item
        # 存在していたら削除
        if os.path.exists(study):
            os.remove(study)
        if os.path.exists(disp):
            os.remove(disp)
    # input['hidden']タグから一番目の要素にIDが入っているらしい
    user_id = req.POST.getlist('user_id')[0]
    print(user_id)

    face_file_list = glob.glob('media/test/**')
    print('顔画像: {}'.format(face_file_list))
    # 画像があれば処理を分ける\
    if len(face_file_list) == 0:
        print('画像無し')
        training_image_flg = False
    else:
        print('画像ある')
        training_image_flg = True

    print('ログイン開始')
    try:
        users = []  # ユーザーの情報
        File = []  # ユーザーの花王
        searchErrMsg = ''  # 検索失敗メッセージ
        print('セッション調教')
        if user_id:
            print(user_id)
            login_key = user_id
            if User.objects.get(schoolnum=login_key):
                users = User.objects.get(schoolnum=login_key)
                print(users.user_name)
            else:
                searchErrMsg = '見つかりませんでした。もう一度入力してください'
            if users.user_name:
                print('認証成功')
                # セッションにIDとして保存
                req.session['id'] = user_id
                sessin_id = req.session['id']
                print('セッション：{}'.format(sessin_id))
                if 'id' in req.session:
                    print('セッション成功')
                    req.session.set_expiry(0)  # 有効期限：ブラウザ閉じるまで
                    print('キー出せ：{}'.format(req.session.keys()))
                    print('ID出せ：{}'.format(req.session.get('id')))
                    # 顔画像ファイルがあるか判定
                    if os.path.isdir('media/face'):
                        # あればスルー
                        if os.path.isdir('media/face'):
                            print('フォルダ検査OK')
                            print('ファイル検査開始')
                            # 対象のフォルダ
                            File = glob.glob('media/face/{}/{}_disp/**'.format(sessin_id, sessin_id))
                            print('フォルダ一覧：{}'.format(File))

    except KeyError:
        print('そんな名前の変数はない')
        pass
    except ObjectDoesNotExist:
        print('検索失敗')
        pass
    except UnboundLocalError:
        print('定義前に変数が使用された')
        pass

    # 削除後の結果を返す
    return render(req,
                  'FaceShoot/user_face.html',
                  {'File': File, 'searchErrMsg': searchErrMsg, 'flg': training_image_flg})


def user_this_time_face_del(req):
    user_id = req.POST.getlist('user_id')[0]
    all_face = req.POST.getlist('all_face')
    print('今回撮影した画像: {}'.format(all_face))
    # 顔認証のノイズになる画像の削除
    for item in req.POST.getlist('del_img'):
        print('削除画像: {}'.format(item))
        # 画像ナンバー抜き出し
        img_Number = item.split('_')[2].split('.')[0]
        # 訓練画像に対応する画像があるか
        study = 'media/face/{}/{}_study/{}.{}'.format(user_id, user_id, user_id, img_Number)
        disp = item
        # 存在していたら削除
        if os.path.exists(study):
            os.remove(study)
        if os.path.exists(disp):
            os.remove(disp)
        # print('削除開始')
        # テスト画像の削除
        test = 'media/test/{}.{}'.format(user_id, img_Number)
        # print(test)
        # 存在していたら削除
        if os.path.exists(test):
            os.remove(test)
            # print('削除成功')

    # input['hidden']タグから一番目の要素にIDが入っているらしい
    user_id = req.POST.getlist('user_id')[0]
    print(user_id)

    # 削除後の顔画像を返す
    del_after_face_img = []
    face_file_list = glob.glob('media/test/**')
    for nokorimono in face_file_list:
        save_face_name = nokorimono.split('\\')[1]
        face_number = save_face_name.split('.')[1]
        # print('学習用顔画像: {}'.format(nokorimono))
        # print('ユーザーID：{}'.format(face_id))
        # print('顔番号：{}'.format(face_number))
        append_face_name = 'media/face/{}/{}_disp/{}_{}.jpg'.format(user_id, user_id, user_id, face_number)
        del_after_face_img.append(append_face_name)
    print('処理完了: {}'.format(del_after_face_img))

    try:
        users = []  # ユーザーの情報
        print('セッション調教')
        if user_id:
            print(user_id)
            login_key = user_id
            if User.objects.get(schoolnum=login_key):
                users = User.objects.get(schoolnum=login_key)
                print(users.user_name)
            if users.user_name:
                print('認証成功')
                # セッションにIDとして保存
                req.session['id'] = user_id
                sessin_id = req.session['id']
                print('セッション：{}'.format(sessin_id))

    except KeyError:
        print('そんな名前の変数はない')
        pass
    except ObjectDoesNotExist:
        print('検索失敗')
        pass
    except UnboundLocalError:
        print('定義前に変数が使用された')
        pass

    return render(req, 'FaceShoot/user_face.html',
                  {'del_after_face_img': del_after_face_img,
                   'user_id': user_id})


def qr_code(req):
    """QRコードを作れる"""
    qr_make = ''  # 作ったQRコードの画像の名前
    qr_text = ''  # QRコードに書き込んだテキスト
    if req.POST:
        qr_text = req.POST['qr_name']
        img = qrcode.make(qr_text)
        qr_make = 'media/{}.png'.format(qr_text)
        img.save(qr_make)
    img = qrcode.make('http://10.128.85.19:8000/Face/top/')
    # print(img.size)
    qr1 = 'media/URL.png'
    img.save(qr1)

    return render(req, 'FaceShoot/QRcode.html',
                  {'qr1': qr1,
                   'qr_make': qr_make,
                   'qr_text': qr_text})


