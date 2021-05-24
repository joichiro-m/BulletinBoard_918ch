#!/usr/bin/env python3
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

import cgi
form_data = cgi.FieldStorage(keep_blank_values = True)

import MySQLdb
con = None
cur = None

import os
from pathlib import Path
env_path = Path('.') / '.env'
from dotenv import load_dotenv
load_dotenv( dotenv_path = env_path, verbose = True )

#トップ画面のHTML出力定義
def print_html():
	print('<!DOCTYPE html>')
	print('<html>')
	print('	<head>')
	print('		<meta charset="UTF-8">')
	print('	</head>')
	print('	<body>')
	print('		<p>ひとこと掲示板</p>')
	print('		<form action="" method="POST">')
	print('			<input type="hidden" name="method_type" value="tweet">')
	print('			<input type="text" name="poster_name" value="" placeholder="なまえ">')
	print('			<br>')
	print('			<textarea name="body_text" value="" placeholder="本文"></textarea>')
	print('			<input type="submit" value="投稿">')
	print('		</form>')
	print('		<hr>')

	#SQLの実行とレコードの取り出し
	sql = "select * from posts"
	cur.execute( sql )
	rows = cur.fetchall()	

	#レコードの表示	
	for row in rows:
		print('<div class="meta">')
		print('<span class="id">' + str(row[ 'id' ]) + '</span>')
		print('<span class="name">' + str(row[ 'name' ]) + '</span>')
		print('<span class="date">' + str(row[ 'created_at' ]) + '</span>')
		print('</div>')
		print('<div class="message"><span>' + str(row[ 'body' ]) + '</span></div>')
		
	print('	</body>')
	print('</html>')

#データベースの更新処理関数
def proceed_methods():
	#フォームの種類取得
	method = form_data[ 'method_type' ].value
	
	#書き込みの場合の処理
	if( method == 'tweet' ):
		#名前の取り出し
		poster_name = form_data[ 'poster_name' ].value
		#投稿内容の取り出し
		body_text = form_data[ 'body_text' ].value
	
		#データベースへの書き込みSQL文作成
		sql = 'insert into posts ( name, body ) values ( %s, %s )'
	
		#データベースの更新処理
		cur.execute( sql, ( poster_name, body_text ) )
		con.commit()
	
	print('<!DOCTYPE html>')
	print('	<html>')
	print('		<head>')
	#ページ更新処理
	print('			<meta http-equiv="refresh" content="5; url=./918ch.py">')
	print('		</head>')
	print('	<body>')
	print('		処理が成功しました。5秒後に元のページに戻ります。')
	print('	</body>')
	print('</html>')



#メイン処理の実行関数
def main():
	print('Content-type: text/html; charset=utf-8')
	print('')
	
	#データベースへ接続
	global con, cur
	try:
		con = MySQLdb.connect(
			host = os.environ.get('db_host'),
			user = str(os.environ.get('db_user')),
			passwd = str(os.environ.get('db_pass')),
			db = str(os.environ.get('db_name')),
			use_unicode = True,
			charset = "utf8"
		)
	
	#データベース接続失敗
	except MySQLdb.Error as e:
		print('データベースへの接続に失敗しました。')
		print( e )
		exit()

	cur = con.cursor( MySQLdb.cursors.DictCursor )

	#フォーム経由のアクセスか判断
	if( 'method_type' in form_data ):
		proceed_methods()
	else:
		print_html()
	
	#データベース終了
	cur.close()
	con.close()
main()
#スクリプト扱いになった際の処理
if __name__ == "__mail__":
	main()
