#!/bin/bash

# Activity Comment API 测试脚本
# 用于测试活动评论相关的所有接口

echo "=========================================="
echo "Activity Comment API 接口测试"
echo "=========================================="

BASE_URL="http://localhost:5000"
ACTID="act_2ab803899022b93d"  # 从测试数据中获取
COMMENTID=""
UID=1000

echo ""
echo "准备工作: 启动 Flask 服务器..."
echo "请确保服务器运行在 http://localhost:5000"
echo ""

# 测试 1: 获取活动评论列表
echo "=========================================="
echo "测试 1: GET /Activity/getCommentList"
echo "=========================================="
echo "请求: GET ${BASE_URL}/Activity/getCommentList?actid=${ACTID}&uid=${UID}"
echo ""

RESPONSE=$(curl -s -X GET "${BASE_URL}/Activity/getCommentList?actid=${ACTID}&uid=${UID}")
echo "响应:"
echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE"

# 提取第一个评论ID用于后续测试
COMMENTID=$(echo "$RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data['data'][0]['commentid'] if data.get('data') else '')" 2>/dev/null)

echo ""
echo "提取的评论ID: $COMMENTID"

# 测试 2: 获取评论回复列表
if [ ! -z "$COMMENTID" ]; then
    echo ""
    echo "=========================================="
    echo "测试 2: GET /Activity/getReplyList"
    echo "=========================================="
    echo "请求: GET ${BASE_URL}/Activity/getReplyList?commentid=${COMMENTID}"
    echo ""
    
    curl -s -X GET "${BASE_URL}/Activity/getReplyList?commentid=${COMMENTID}" | python3 -m json.tool 2>/dev/null
fi

# 测试 3: 获取新评论列表
echo ""
echo "=========================================="
echo "测试 3: POST /Activity/getNewCommentList"
echo "=========================================="
echo "请求: POST ${BASE_URL}/Activity/getNewCommentList"
echo "数据: {\"actid\": \"${ACTID}\", \"commentid\": \"${COMMENTID}\"}"
echo ""

curl -s -X POST "${BASE_URL}/Activity/getNewCommentList" \
  -H "Content-Type: application/json" \
  -d "{\"actid\": \"${ACTID}\", \"commentid\": \"${COMMENTID}\"}" | python3 -m json.tool 2>/dev/null

# 测试 4: 获取用户相关回复
echo ""
echo "=========================================="
echo "测试 4: POST /Activity/getCommentReplyList"
echo "=========================================="
echo "请求: POST ${BASE_URL}/Activity/getCommentReplyList"
echo "数据: {\"uid\": ${UID}}"
echo ""

curl -s -X POST "${BASE_URL}/Activity/getCommentReplyList" \
  -H "Content-Type: application/json" \
  -d "{\"uid\": ${UID}}" | python3 -m json.tool 2>/dev/null

# 测试 5: 评论点赞 (需要 token，这里模拟)
echo ""
echo "=========================================="
echo "测试 5: POST /Activity/updateCommentLike"
echo "=========================================="
echo "请求: POST ${BASE_URL}/Activity/updateCommentLike"
echo "数据: {\"commentid\": \"${COMMENTID}\", \"uid\": 9999, \"likeuid\": ${UID}, \"actid\": \"${ACTID}\"}"
echo ""

if [ ! -z "$COMMENTID" ]; then
    curl -s -X POST "${BASE_URL}/Activity/updateCommentLike" \
      -H "Content-Type: application/json" \
      -d "{\"commentid\": \"${COMMENTID}\", \"uid\": 9999, \"likeuid\": ${UID}, \"actid\": \"${ACTID}\"}" | python3 -m json.tool 2>/dev/null
fi

# 测试 6: 取消评论点赞
echo ""
echo "=========================================="
echo "测试 6: POST /Activity/delCommentLike"
echo "=========================================="
echo "请求: POST ${BASE_URL}/Activity/delCommentLike"
echo "数据: {\"commentid\": \"${COMMENTID}\", \"uid\": 9999}"
echo ""

if [ ! -z "$COMMENTID" ]; then
    curl -s -X POST "${BASE_URL}/Activity/delCommentLike" \
      -H "Content-Type: application/json" \
      -d "{\"commentid\": \"${COMMENTID}\", \"uid\": 9999}" | python3 -m json.tool 2>/dev/null
fi

echo ""
echo "=========================================="
echo "测试完成！"
echo "=========================================="
echo ""
echo "使用说明:"
echo "1. 确保 Flask 服务器运行在 http://localhost:5000"
echo "2. 运行命令: bash test_comment_api_curl.sh"
echo "3. 查看各接口的响应结果"
echo ""
