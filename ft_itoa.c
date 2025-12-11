/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_itoa.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mel-shdo <mustafa.el-shdouh@student.42.    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/11 20:02:47 by mel-shdo          #+#    #+#             */
/*   Updated: 2025/12/11 20:28:24 by mel-shdo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdlib.h>
#include <stddef.h>
#include "libft.h"
//#include <stdio.h>
//#include <limits.h>

static int	getlength(int n)
{
	int	length;

	length = 0;
	if (n <= 0)
		length = 1;
	while (n != 0)
	{
		n = n / 10;
		length++;
	}
	return (length);
}

char	*ft_itoa(int n)
{
	char	*str;
	int		length;
	long	num;

	num = n;
	length = getlength(n);
	str = (char *)malloc(sizeof(char) * (length + 1));
	if (!str)
		return (NULL);
	str[length] = '\0';
	length--;
	if (num == 0)
		str[0] = '0';
	if (num < 0)
	{
		str[0] = '-';
		num = -num;
	}
	while (num > 0)
	{
		str[length] = (num % 10) + '0';
		num = num / 10;
		length--;
	}
	return (str);
}

/*int	main(void)
{
	char *res;

	// Test 1: Regular number
	res = ft_itoa(1234);
	printf("1234 -> %s\n", res);
	free(res);

	// Test 2: Negative number
	res = ft_itoa(-42);
	printf("-42 -> %s\n", res);
	free(res);

	// Test 3: Zero
	res = ft_itoa(0);
	printf("0 -> %s\n", res);
	free(res);

	// Test 4: INT_MIN (The Boss Fight)
	res = ft_itoa(-2147483648);
	printf("INT_MIN -> %s\n", res); // Should be "-2147483648"
	free(res);

	// Test 5: INT_MAX
	res = ft_itoa(2147483647);
	printf("INT_MAX -> %s\n", res);
	free(res);

	return (0);
}*/