
def call(hoseRaceResults, raceResult):
	""" グラフを描画する """

	# 日本語フォントを有効にする
	matplotlib.rcParams['font.sans-serif'] = 'MigMix 1P'   

	# グラフプロット
	x = [ hoseRaceResult.RaceResult.RPCI for hoseRaceResult in hoseRaceResults ]
	y = [ hoseRaceResult.RaceResult.ave_1F for hoseRaceResult in hoseRaceResults ]
	names = [ f'{hoseRaceResult.RaceResult.date} {hoseRaceResult.RaceResult.name} {hoseRaceResult.RaceResult.cource_condition} {hoseRaceResult.HoseRaceResult.time_diff}' for hoseRaceResult in hoseRaceResults ]

	""" 
			着差ごとにplotは色分けする 
			　・1着 -> 黄色
			　・~0.4s 差 -> 緑
			　・0.4s~1.0s 差 -> 青
			　・1.0s〜 差 -> 灰色    
	"""

	colorTbl = []
	edgeColorTbl = []
	count = 0
	for index, hoseRaceResult in enumerate(hoseRaceResults):
			try:
					if hoseRaceResult.HoseRaceResult.rank == '1':
							colorTbl.append('yellow')
					elif float(hoseRaceResult.HoseRaceResult.time_diff) <= 0.4:
							colorTbl.append('green')
					elif float(hoseRaceResult.HoseRaceResult.time_diff) <= 1.0:
							colorTbl.append('blue')
					else:
							colorTbl.append('gray')
					
					# 近5走までは散布図の縁を赤色
					# 近10走までは散布図の縁をオレンジ色にする。
					if count < 5:
							edgeColorTbl.append('red')
					elif count < 10:
							edgeColorTbl.append('black')
					else:
							edgeColorTbl.append('white')
					
					count += 1

			except ValueError as e:
					print(f'race_id: {hoseRaceResult.HoseRaceResult.race_id} 競争除外レースのため結果から外します。')
					# グラフから競争除外のレースのプロットを除外
					del x[index]
					del y[index]
					del names[index]
					continue            

	# RaceResultsを受け取った場合はプロットする
	if raceResults != None:
			for raceResult in raceResults:
					x.append(raceResult.RPCI)
					y.append(raceResult.ave_1F)
					names.append(f'{raceResult.date} {raceResult.name} {raceResult.cource_condition}')
					colorTbl.append("red")
					edgeColorTbl.append('white')
	
			# 中央値を求めてプロットする
			x_median = np.median([ raceResult.RPCI for raceResult in raceResults ])
			y_median = np.median([ raceResult.ave_1F for raceResult in raceResults ] )

	fig,ax = plt.subplots()
	sc = plt.scatter(x, y, c=colorTbl, linewidth=1, edgecolors=edgeColorTbl)

	# プロットにホバーした時、凡例を表示させる
	annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
									bbox=dict(boxstyle="round", fc="w"),
									arrowprops=dict(arrowstyle="->"))

	annot.set_visible(False)

	def update_annot(ind):

			pos = sc.get_offsets()[ind["ind"][0]]
			annot.xy = pos
			text = "{}, {}".format(" ".join(list(map(str,ind["ind"]))), 
													" ".join([names[n] for n in ind["ind"]]))
			annot.set_text(text)
			annot.get_bbox_patch().set_facecolor(colorTbl[ind["ind"][0]])
			annot.get_bbox_patch().set_alpha(0.4)


	def hover(event):
			vis = annot.get_visible()
			if event.inaxes == ax:
					cont, ind = sc.contains(event)
					if cont:
							update_annot(ind)
							annot.set_visible(True)
							fig.canvas.draw_idle()
					else:
							if vis:
									annot.set_visible(False)
									fig.canvas.draw_idle()

	fig.canvas.mpl_connect("motion_notify_event", hover)

	# グラフの体裁を整える
	plt.xlabel('RPCI')
	plt.ylabel('ave-1F')
	plt.title(f'{hoseRaceResults[0].Hose.name} \n RPCI x ave-1F マトリクス')
	plt.xlim(45, 60)
	plt.ylim(11, 13)
	plt.savefig('test_hoseRaceResult.png', dpi=300)

	plt.hlines(y_median, 30, 70, "red", linestyles='dashed')
	plt.vlines(x_median, 10, 14, "red", linestyles='dashed') 
	# plt.hlines(12.26, 30, 70, "red", linestyles='dashed')
	# plt.vlines(54.0, 10, 14, "red", linestyles='dashed') 

	plt.hlines(11.80, 30, 70, "blue", linestyles='dashed') 
	plt.hlines(12.00, 30, 70, "blue", linestyles='dashed') 
	plt.vlines(47, 10, 14, "blue", linestyles='dashed') 
	plt.vlines(50.20, 10, 14, "blue", linestyles='dashed') 

	plt.show()